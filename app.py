from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from groq import Groq


app = Flask(__name__)
# Security key for session management (change this in production)
app.config['SECRET_KEY'] = os.environ.get('SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pickone.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirects here if unauthorized users try to access protected routes
login_manager.login_message_category = "error"

# --- DATABASE MODEL ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(50), unique=True, nullable=False) 
    user_email = db.Column(db.String(120), nullable=False)
    user_role = db.Column(db.String(20), nullable=False) 
    password_hash = db.Column(db.String(256), nullable=False)
    
    # --- NEW: Subscription & Trial Data ---
    # Automatically records when they created their account
    trial_start_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Tiers: 'trial', 'monthly', '3-month', '12-month', 'lifetime'
    subscription_tier = db.Column(db.String(50), default='trial') 
    subscription_end_date = db.Column(db.DateTime, nullable=True)

# --- DATABASE MODELS ---
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True, nullable=False) 
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    blood_type = db.Column(db.String(5))
    
    # --- NEW FIELDS FOR PHASE 1 ---
    allergies = db.Column(db.Text)
    active_medications = db.Column(db.Text)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False) 
    doctor_name = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.String(50), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Approved')

class VisitRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), db.ForeignKey('patient.patient_id'), nullable=False)
    recorded_by = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Telemetry Data
    bp = db.Column(db.String(20))
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    spo2 = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    nurse_notes = db.Column(db.Text)
    
    # --- NEW: Doctor Data ---
    diagnosis = db.Column(db.Text)
    prescriptions = db.Column(db.Text)

    patient = db.relationship('Patient', backref=db.backref('visit_records', lazy=True))


with app.app_context():
    db.create_all()


# --- HELPER: CHECK SUBSCRIPTION VALIDITY ---
def check_active_subscription(user):
    """Returns True if the user has an active trial or paid subscription."""
    if user.subscription_tier == 'lifetime':
        return True
    
    now = datetime.utcnow()
    
    # Check 60-day trial
    if user.subscription_tier == 'trial':
        trial_end = user.trial_start_date + timedelta(days=0)
        if now < trial_end:
            return True
        return False # Trial expired
        
    # Check paid subscriptions
    if user.subscription_end_date and now < user.subscription_end_date:
        return True
        
    return False

# --- NEW ROUTE: SUPPORT PAGE ---
@app.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # NOTE: To actually send an email to eg@gmail.com, you would use Flask-Mail 
        # or smtplib here with your SMTP credentials. For now, we simulate success.
        
        print(f"--- SIMULATED EMAIL TO eg@gmail.com ---")
        print(f"From: {current_user.user_email}")
        print(f"Subject: {subject}\nMessage: {message}")
        print(f"---------------------------------------")
        
        flash('Your message has been sent to our support team. We will reply shortly!', 'success')
        return redirect(url_for('support'))
        
    return render_template('support/support.html')

# --- NEW ROUTE: PRICING PAGE ---
@app.route('/pricing')
@login_required
def pricing():
    return render_template('pricing/pricing.html')

# --- NEW ROUTE: SIMULATED CHECKOUT ---
@app.route('/checkout/<tier>')
@login_required
def simulate_checkout(tier):
    """A dummy route to simulate purchasing a subscription."""
    now = datetime.utcnow()
    current_user.subscription_tier = tier
    
    if tier == 'monthly':
        current_user.subscription_end_date = now + timedelta(days=30)
    elif tier == '3-month':
        current_user.subscription_end_date = now + timedelta(days=90)
    elif tier == '12-month':
        current_user.subscription_end_date = now + timedelta(days=365)
    elif tier == 'lifetime':
        current_user.subscription_end_date = None # Never expires
        
    db.session.commit()
    flash(f'Successfully upgraded to the {tier.capitalize()} plan!', 'success')
    return redirect_based_on_role(current_user.user_role)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTHENTICATION ROUTES ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = request.form.get('id')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')

        # Check if user ID already exists
        if User.query.filter_by(user_id=user_id).first():
            flash('User ID already exists. Please choose another or login.', 'error')
            return redirect(url_for('register'))

        # Hash password and create user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(user_name=name, user_id=user_id, user_email=email, user_role=role, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.', 'error')
            return redirect(url_for('register'))

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, skip the login page
    if current_user.is_authenticated:
        return redirect_based_on_role(current_user.user_role)

    if request.method == 'POST':
        role = request.form.get('role')
        user_id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.filter_by(user_id=user_id, user_role=role).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.user_name}!', 'success')
            return redirect_based_on_role(user.user_role)
        else:
            flash('Invalid User ID, Password, or Role mismatch.', 'error')
            return redirect(url_for('login'))

    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# --- HELPER FUNCTION ---
def redirect_based_on_role(role):
    """Routes the user to the correct dashboard based on their role."""
    if role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    elif role == 'nurse':
        return redirect(url_for('nurse_dashboard'))
    elif role == 'patient':
        return redirect(url_for('patient_dashboard'))
    return redirect(url_for('login'))

# --- DASHBOARD ROUTES ---
# Initialize Groq Client
groq_client = Groq(api_key=os.environ.get("PICKONEMED_KEY"))

def generate_ai_summary(patient, records):
    """Generates an on-the-fly AI summary of the patient's medical history."""
    if not os.environ.get("PICKONEMED_KEY"):
        return "Groq API Key missing. Please set GROQ_API_KEY environment variable to view AI summaries."

    history = f"Patient: {patient.first_name} {patient.last_name}, Age: {patient.dob}, Gender: {patient.gender}, Blood: {patient.blood_type}.\nRecent Records:\n"
    for r in records[:5]: # Send last 5 records
        history += f"- {r.timestamp.strftime('%Y-%m-%d')}: BP {r.bp}, HR {r.heart_rate}, Temp {r.temperature}. "
        if r.diagnosis: history += f"Diag: {r.diagnosis}. "
        if r.prescriptions: history += f"Rx: {r.prescriptions}. "
        history += "\n"

    prompt = f"Provide a brief, 3-sentence clinical overview and a short bulleted list of 'Automated Insights' based on this history:\n{history}"

    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a helpful clinical AI assistant."},
                      {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return "AI Summary temporarily unavailable."


def check_prescription_conflicts(patient, records, new_rx, diagnosis):
    """Uses Groq to verify if a new prescription conflicts with patient history."""
    if not os.environ.get("PICKONEMED_KEY") or not new_rx:
        return "SAFE" # Bypass if no key or no prescription

    past_rx = [r.prescriptions for r in records if r.prescriptions]
    prompt = f"""
    Patient History of Prescriptions: {', '.join(past_rx) if past_rx else 'None'}
    New Diagnosis: {diagnosis}
    New Prescription: {new_rx}

    Are there any severe drug interactions or contraindications? 
    If safe, reply ONLY with the word 'SAFE'.
    If there is a conflict, reply with 'WARNING:' followed by a 1-sentence explanation.
    """
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a pharmacological AI assistant."},
                      {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception:
        return "SAFE"


@app.route('/doctor/dashboard', methods=['GET', 'POST'])
@login_required
def doctor_dashboard():
    if current_user.user_role != 'doctor':
        flash('Unauthorized access.', 'error')
        return redirect_based_on_role(current_user.user_role)
    
    if not check_active_subscription(current_user):
        flash('Your 60-day trial has expired. Please upgrade your subscription to continue.', 'error')
        return redirect(url_for('pricing'))

    search_id = request.args.get('search_id')
    patient_data = None
    records = []
    ai_summary = None
    trend_data = {}

    # --- POST: ADD DIAGNOSIS & PRESCRIPTION ---
    if request.method == 'POST':
        p_id = request.form.get('patient_id')
        diagnosis = request.form.get('diagnosis')
        prescriptions = request.form.get('prescriptions')

        pat = Patient.query.filter_by(patient_id=p_id).first()
        if pat:
            recs = VisitRecord.query.filter_by(patient_id=p_id).order_by(VisitRecord.timestamp.desc()).all()
            
            # 1. Check for Conflicts via AI
            conflict_check = check_prescription_conflicts(pat, recs, prescriptions, diagnosis)
            
            if "WARNING" in conflict_check.upper():
                flash(f'⚠️ AI Conflict Alert: {conflict_check}', 'error')
                return redirect(url_for('doctor_dashboard', search_id=p_id))

            # 2. Save new Doctor Record
            new_record = VisitRecord(
                patient_id=p_id,
                recorded_by=f"Dr. {current_user.user_name}",
                diagnosis=diagnosis,
                prescriptions=prescriptions,
                nurse_notes="Doctor Consultation"
            )
            db.session.add(new_record)
            db.session.commit()
            flash('Diagnosis and prescriptions saved successfully.', 'success')
            
        return redirect(url_for('doctor_dashboard', search_id=p_id))

    # --- GET: SEARCH & LOAD PATIENT ---
    if search_id:
        patient_data = Patient.query.filter_by(patient_id=search_id).first()
        if patient_data:
            # Ascending order for charts
            records = VisitRecord.query.filter_by(patient_id=search_id).order_by(VisitRecord.timestamp.asc()).all()
            
            # Build JSON dictionary for Chart.js
            trend_data = {
                "labels": [r.timestamp.strftime('%b %d') for r in records if r.heart_rate],
                "heart_rate": [r.heart_rate for r in records if r.heart_rate],
                "temperature": [r.temperature for r in records if r.temperature],
                "weight": [r.weight for r in records if r.weight],
                "spo2": [r.spo2 for r in records if r.spo2]
            }

            # Descending order for Summary and History reading
            records.reverse()
            ai_summary = generate_ai_summary(patient_data, records)
        else:
            flash(f'Patient ID {search_id} not found in system.', 'error')

    # Inside doctor_dashboard (GET block)
    appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()
    
    return render_template('dashboards/doctor.html', 
                           patient=patient_data, 
                           records=records,
                           ai_summary=ai_summary,
                           trend_data=trend_data,
                           appointments=appointments,
                           search_id=search_id)

@app.route('/api/doctor/chat', methods=['POST'])
@login_required
def doctor_chat_api():
    # Security check
    if current_user.user_role != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    p_id = data.get('patient_id')
    user_message = data.get('message')

    if not p_id or not user_message:
        return jsonify({'error': 'Missing patient ID or message'}), 400

    # Fetch patient data and history
    patient = Patient.query.filter_by(patient_id=p_id).first()
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    records = VisitRecord.query.filter_by(patient_id=p_id).order_by(VisitRecord.timestamp.asc()).all()

    # Build the clinical context for the AI
    history = f"Patient: {patient.first_name} {patient.last_name}, DOB: {patient.dob}, Gender: {patient.gender}, Blood: {patient.blood_type}.\nHistorical Records:\n"
    for r in records:
        history += f"- Date: {r.timestamp.strftime('%Y-%m-%d')}. Vitals: BP {r.bp}, HR {r.heart_rate}, Temp {r.temperature}. "
        if r.diagnosis: history += f"Diagnosis: {r.diagnosis}. "
        if r.prescriptions: history += f"Prescriptions: {r.prescriptions}. "
        history += "\n"

    prompt = f"""
    You are a medical AI assistant helping Dr. {current_user.user_name}.
    Here is the data for the current patient ({p_id}):
    {history}
    
    The doctor asks: "{user_message}"
    
    Provide a concise, highly professional clinical response based ONLY on the provided data.
    """

    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a clinical AI assistant. Keep responses under 4 sentences unless specifically asked for more detail. Format clearly."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2, # Low temperature for more factual, less creative responses
            max_tokens=300
        )
        ai_reply = response.choices[0].message.content
        return jsonify({'response': ai_reply})
        
    except Exception as e:
        print(f"Groq API Error: {e}")
        return jsonify({'error': 'AI processing failed. Please check your Groq API key.'}), 500

@app.route('/nurse/dashboard', methods=['GET', 'POST'])
@login_required
def nurse_dashboard():
    if current_user.user_role != 'nurse':
        flash('Unauthorized access. You are not a nurse.', 'error')
        return redirect_based_on_role(current_user.user_role)
    
    if not check_active_subscription(current_user):
        flash('Your 60-day trial has expired. Please upgrade your subscription to continue.', 'error')
        return redirect(url_for('pricing'))

    # --- 1. HANDLE SAVING NEW VITALS (POST) ---
    if request.method == 'POST':
        p_id = request.form.get('patient_id')
        
        # Verify patient exists before saving records
        patient = Patient.query.filter_by(patient_id=p_id).first()
        if not patient:
            flash(f'Cannot save record: Patient ID {p_id} not found in system.', 'error')
            return redirect(url_for('nurse_dashboard'))

        # Create new visit record
        new_record = VisitRecord(
            patient_id=p_id,
            recorded_by=f"Nurse {current_user.user_name}",
            bp=request.form.get('bp'),
            heart_rate=request.form.get('heart_rate'),
            temperature=request.form.get('temperature'),
            spo2=request.form.get('spo2'),
            weight=request.form.get('weight'),
            height=request.form.get('height'),
            nurse_notes=request.form.get('nurse_notes')
        )
        try:
            db.session.add(new_record)
            db.session.commit()
            flash('Vitals successfully saved to patient record.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error saving records.', 'error')
            
        # Redirect to the same patient to see the updated table
        return redirect(url_for('nurse_dashboard', search_id=p_id))

    # --- 2. HANDLE PATIENT SEARCH (GET) ---
    search_id = request.args.get('search_id')
    patient_data = None
    vitals_history = []

    if search_id:
        patient_data = Patient.query.filter_by(patient_id=search_id).first()
        if patient_data:
            # Fetch all records for this patient, newest first
            vitals_history = VisitRecord.query.filter_by(patient_id=search_id).order_by(VisitRecord.timestamp.desc()).all()
        else:
            flash(f'Patient {search_id} not found.', 'error')

    

    # Inside nurse_dashboard (GET block)
    appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()

    return render_template('dashboards/nurse.html', 
                           patient=patient_data, 
                           vitals=vitals_history, 
                           appointments=appointments,
                           search_id=search_id)

@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if current_user.user_role != 'patient':
        flash('Unauthorized access. You are not a patient.', 'error')
        return redirect_based_on_role(current_user.user_role)
    
    if not check_active_subscription(current_user):
        flash('Your 60-day trial has expired. Please upgrade your subscription to continue.', 'error')
        return redirect(url_for('pricing'))

    p_id = current_user.user_id

    # 1. Fetch Patient Profile
    patient = Patient.query.filter_by(patient_id=p_id).first()
    
    # Calculate Age
    age = "--"
    if patient and patient.dob:
        try:
            dob_date = datetime.strptime(patient.dob, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        except ValueError:
            age = patient.dob # Fallback if format is weird

    # 2. Fetch Upcoming Appointments
    appointments = Appointment.query.filter_by(patient_id=p_id).order_by(Appointment.appointment_date.asc()).all()

    # 3. Fetch Visit Records (Descending for Latest Vitals and Notes)
    records_desc = VisitRecord.query.filter_by(patient_id=p_id).order_by(VisitRecord.timestamp.desc()).all()
    
    latest_vitals = records_desc[0] if records_desc else None
    recent_notes = records_desc[:3] # Grab the last 3 visits

    # 4. Prepare Trend Data for Charts (Ascending order)
    records_asc = list(reversed(records_desc))
    trend_data = {
        "labels": [r.timestamp.strftime('%b %d') for r in records_asc if r.weight or r.heart_rate or r.temperature],
        "weight": [r.weight for r in records_asc if r.weight],
        "heart_rate": [r.heart_rate for r in records_asc if r.heart_rate],
        "temperature": [r.temperature for r in records_asc if r.temperature]
    }

    return render_template('dashboards/patient.html', 
                           patient=patient, 
                           age=age,
                           latest_vitals=latest_vitals, 
                           recent_notes=recent_notes, 
                           appointments=appointments, 
                           trend_data=trend_data,
                           datetime=datetime) 

@app.route('/api/update_patient_profile', methods=['POST'])
@login_required
def update_patient_profile():
    # 1. Security Check: Only Doctors and Nurses can edit profiles
    if current_user.user_role not in ['doctor', 'nurse']:
        flash('Unauthorized to edit patient profiles.', 'error')
        return redirect(url_for('login'))

    p_id = request.form.get('patient_id')
    patient = Patient.query.filter_by(patient_id=p_id).first()
    
    if patient:
        # 2. Update Database Fields
        patient.dob = request.form.get('dob')
        patient.gender = request.form.get('gender')
        patient.blood_type = request.form.get('blood_type')
        patient.allergies = request.form.get('allergies')
        patient.active_medications = request.form.get('active_medications')
        
        try:
            db.session.commit()
            flash('Patient profile updated successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating patient profile.', 'error')
    else:
        flash('Patient not found.', 'error')
        
    # 3. Smart Redirect: Send them back to the dashboard they came from
    if current_user.user_role == 'doctor':
        return redirect(url_for('doctor_dashboard', search_id=p_id))
    else:
        return redirect(url_for('nurse_dashboard', search_id=p_id))
    
@app.route('/api/update_appointment_status', methods=['POST'])
@login_required
def update_appointment_status():
    if current_user.user_role not in ['doctor', 'nurse']:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('login'))

    appt_id = request.form.get('appointment_id')
    new_status = request.form.get('status') # 'Approved' or 'Cancelled'

    appt = Appointment.query.get(appt_id)
    if appt:
        appt.status = new_status
        db.session.commit()
        flash(f'Appointment marked as {new_status}.', 'success')
    else:
        flash('Appointment not found.', 'error')

    # Keep the user on their respective dashboard
    if current_user.user_role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    return redirect(url_for('nurse_dashboard'))

@app.route('/schedule_appointment', methods=['POST'])
@login_required
def schedule_appointment():
    # 1. Security Check: Only patients should be booking appointments this way
    if current_user.user_role != 'patient':
        flash('Only patients can schedule appointments from this portal.', 'error')
        return redirect(url_for('login'))

    # 2. Grab the data from the modal form
    doctor_name = request.form.get('doctor_name')
    app_date = request.form.get('appointment_date')
    app_time = request.form.get('appointment_time')
    reason = request.form.get('reason')

    # 3. Create the new appointment record
    new_appointment = Appointment(
        patient_id=current_user.user_id,
        doctor_name=doctor_name,
        appointment_date=app_date,
        appointment_time=app_time,
        reason=reason,
        status='Pending'  # Requires staff approval
    )

    # 4. Save to Database
    try:
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment request submitted successfully! It is currently Pending approval.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while scheduling the appointment.', 'error')

    # 5. Redirect back to the patient dashboard to see the new entry
    return redirect(url_for('patient_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)