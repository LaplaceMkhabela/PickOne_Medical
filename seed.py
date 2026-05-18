from app import app, db, Patient, VisitRecord, Appointment, User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_database():
    with app.app_context():
        # Ensure tables exist with the newest schema
        db.create_all()
        print("Database tables verified.")

        # --- 0. MOCK USERS (Login Accounts) ---
        # We create login profiles so you don't have to manually register them to test
        mock_users = [
            # Staff Accounts
            {'name': 'Dr. Sarah Jenkins', 'id': 'DOC-100', 'email': 'dr.jenkins@pickone.com', 'role': 'doctor'},
            {'name': 'Dr. Marcus', 'id': 'DOC-101', 'email': 'dr.marcus@pickone.com', 'role': 'doctor'},
            {'name': 'Nurse Admin', 'id': 'NUR-100', 'email': 'nurse.admin@pickone.com', 'role': 'nurse'},
            
            # Patient Accounts
            {'name': 'Sarah Jenkins', 'id': 'PAT-1042', 'email': 'sarah.j@example.com', 'role': 'patient'},
            {'name': 'Marcus Chen', 'id': 'PAT-0891', 'email': 'marcus.c@example.com', 'role': 'patient'},
            {'name': 'Elena Rodriguez', 'id': 'PAT-2055', 'email': 'elena.r@example.com', 'role': 'patient'}
        ]

        # Use a simple, uniform password for all test accounts
        default_password = generate_password_hash('password123', method='pbkdf2:sha256')

        for u_data in mock_users:
            if not User.query.filter_by(user_id=u_data['id']).first():
                new_user = User(
                    user_name=u_data['name'],
                    user_id=u_data['id'],
                    user_email=u_data['email'],
                    user_role=u_data['role'],
                    password_hash=default_password
                )
                db.session.add(new_user)
        
        db.session.commit()
        print("Mock Users added successfully. (Default Password for all: password123)")

        # --- 1. MOCK PATIENTS (Profile Data) ---
        mock_patients = [
            {
                'id': 'PAT-1042', 'first': 'Sarah', 'last': 'Jenkins', 
                'dob': '1981-05-14', 'gender': 'F', 'blood': 'A+',
                'allergies': 'Penicillin, Peanuts',
                'active_medications': 'Lisinopril 10mg (Daily), Metformin 500mg (BID)'
            },
            {
                'id': 'PAT-0891', 'first': 'Marcus', 'last': 'Chen', 
                'dob': '1975-11-22', 'gender': 'M', 'blood': 'O-',
                'allergies': 'None',
                'active_medications': 'Albuterol Inhaler (As needed)'
            },
            {
                'id': 'PAT-2055', 'first': 'Elena', 'last': 'Rodriguez', 
                'dob': '1992-03-08', 'gender': 'F', 'blood': 'B+',
                'allergies': 'Latex, Sulfa Drugs',
                'active_medications': 'None'
            }
        ]

        for p_data in mock_patients:
            if not Patient.query.filter_by(patient_id=p_data['id']).first():
                new_patient = Patient(
                    patient_id=p_data['id'],
                    first_name=p_data['first'],
                    last_name=p_data['last'],
                    dob=p_data['dob'],
                    gender=p_data['gender'],
                    blood_type=p_data['blood'],
                    allergies=p_data['allergies'],
                    active_medications=p_data['active_medications']
                )
                db.session.add(new_patient)
        
        db.session.commit()
        print("Mock Patient Profiles added successfully.")

        # --- 2. MOCK UPCOMING APPOINTMENTS ---
        today = datetime.now()
        
        mock_appointments = [
            Appointment(
                patient_id='PAT-1042', doctor_name='Dr. Sarah Jenkins',
                appointment_date=(today + timedelta(days=5)).strftime('%Y-%m-%d'),
                appointment_time='10:00 AM', reason='Routine Diabetes Follow-up', status='Approved'
            ),
            Appointment(
                patient_id='PAT-1042', doctor_name='Dr. Marcus',
                appointment_date=(today + timedelta(days=21)).strftime('%Y-%m-%d'),
                appointment_time='02:30 PM', reason='Cardiology Consult', status='Pending'
            ),
            Appointment(
                patient_id='PAT-0891', doctor_name='Dr. Sarah Jenkins',
                appointment_date=(today + timedelta(days=2)).strftime('%Y-%m-%d'),
                appointment_time='09:15 AM', reason='Post-infection checkup', status='Approved'
            )
        ]

        if Appointment.query.count() == 0:
            db.session.bulk_save_objects(mock_appointments)
            db.session.commit()
            print("Upcoming Appointments generated.")

        # --- 3. MOCK HISTORICAL VISIT RECORDS ---
        mock_records = [
            # Sarah Jenkins (PAT-1042)
            VisitRecord(patient_id='PAT-1042', recorded_by='Dr. Marcus', timestamp=today - timedelta(days=90), bp='140/90', heart_rate=82, temperature=36.6, spo2=98, weight=75.0, height=165, nurse_notes='Patient reports frequent dizziness and fatigue.', diagnosis='Essential Hypertension. High fasting blood glucose indicating early Type 2 Diabetes.', prescriptions='Lisinopril 10mg once daily.'),
            VisitRecord(patient_id='PAT-1042', recorded_by='Dr. Marcus', timestamp=today - timedelta(days=45), bp='135/85', heart_rate=78, temperature=36.5, spo2=99, weight=73.5, height=165, nurse_notes='Follow-up on BP. Patient trying to improve diet.', diagnosis='Hypertension showing slight improvement. Confirmed Type 2 Diabetes after A1C test.', prescriptions='Metformin 500mg twice daily with meals. Continue Lisinopril.'),
            VisitRecord(patient_id='PAT-1042', recorded_by='Nurse Admin', timestamp=today - timedelta(days=2), bp='125/82', heart_rate=74, temperature=36.7, spo2=98, weight=71.2, height=165, nurse_notes='Routine triage check. Patient feels much better.', diagnosis='', prescriptions=''),

            # Marcus Chen (PAT-0891)
            VisitRecord(patient_id='PAT-0891', recorded_by='Nurse Admin', timestamp=today - timedelta(days=14), bp='120/80', heart_rate=88, temperature=38.2, spo2=94, weight=82.0, height=180, nurse_notes='Patient presents with high fever, persistent cough.', diagnosis='', prescriptions=''),
            VisitRecord(patient_id='PAT-0891', recorded_by='Dr. Sarah Jenkins', timestamp=today - timedelta(days=14), bp='122/82', heart_rate=85, temperature=38.0, spo2=95, weight=82.0, height=180, nurse_notes='Doctor consultation.', diagnosis='Acute Bronchitis.', prescriptions='Amoxicillin 500mg every 8 hours for 7 days. Albuterol inhaler PRN.'),
            VisitRecord(patient_id='PAT-0891', recorded_by='Dr. Sarah Jenkins', timestamp=today - timedelta(days=2), bp='118/78', heart_rate=70, temperature=36.6, spo2=99, weight=81.5, height=180, nurse_notes='Follow-up. Lungs clear.', diagnosis='Resolved Bronchitis.', prescriptions='Discontinue Amoxicillin.')
        ]

        if VisitRecord.query.count() == 0:
            db.session.bulk_save_objects(mock_records)
            db.session.commit()
            print("Historical Telemetry & Diagnoses generated.")

        print("\n✅ Database Seeding Complete!")

if __name__ == '__main__':
    seed_database()