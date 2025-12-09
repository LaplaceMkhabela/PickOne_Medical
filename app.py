from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json,os
from database.data import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "pick397df4w6tg"

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    user_role = db.Column(db.String(250), unique=False, nullable=False)
    user_email = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.String(250), nullable=False)
    user_password = db.Column(db.String(250), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transition/<msg>/<links>')
def transition(msg,links):
    return render_template('transition.html',msg=msg,links=links)

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

    if Users.query.filter_by(user_id=id).first():
        return render_template('transition.html',msg='Username ID  already taken!')

    password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    new_user = Users(user_name=name,user_role=role,user_email=email,user_id=id,user_password=password_hash)

    try:
        db.session.add(new_user)
        db.session.commit()

        return render_template('transition.html',msg='Account Created Successfully',links='/dashboard')
    except:
        return render_template('transition.html',msg='Failed to create Account',links='/register')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_role = request.form['role']
        user_id = request.form['id']
        user_password = request.form['password']

    user = Users.query.filter_by(user_id=user_id).first()

    if user and check_password_hash(user.user_password,user_password):
        login_user(user)
        return redirect(url_for('welcome',name=user.user_name)) 
    else:
        msg = 'Invalid login details'
        links = 'i'
        return redirect(url_for('transition',msg=msg,links=links))

@app.route('/welcome/<name>')
def welcome(name):
    return render_template('welcome.html',name=name)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',current_user=current_user)

@app.route("/mock/patients")
def mock_patients():
    Base.metadata.create_all(engine)

    with open(os.path.join('database', "mock_patient_data.json"), "r") as file_data:
        data = json.loads(file_data.read())
        patient_list = data["patients"]
        
        for patient in patient_list:
            history = patient['history']
            new_history = ''

            for record in history:
                new_record = ''
                new_record += record['date']
                new_record += record['reason']
                new_record += record['doctor']
                new_record += record['notes']

                new_history += ''.join(new_record)


            p = create_patient(patient_db, patient['name'],patient['email'],patient['age'],patient['gender'],patient['bp'],patient['weight'],patient['bmi'],patient['temp'],patient['pulse'],patient['hbmp'],new_history)
            print(f'created-{p.name}')

    return "Created all patient records"

@app.route('/search',methods=['GET','POST'])
def search():
    id = request.form['query']
    data = []
    patient = get_patient(patient_db,str(id))
    if get_patient(patient_db,str(id)):
        patient_results = {
            'name': patient.name,
            'gender' : patient.gender,
            'id' : patient.id,
            'email': patient.email,
            'weight': patient.weight,
            'bp': patient.bp,
            'bmi': patient.bmi,
            'temp':patient.temp,
            'pulse':patient.pulse,
            'hbpm': patient.hbpm
        }

    
    data.append(patient)
    print(data)
    return render_template('search.html',data=data)

        

@app.route('/patient/dashboard')
def patient_dashboard():
    return render_template('patient_dashboard.html')

@app.route('/patient/reports')
def patient_reports():
    return render_template('reports.html')

@app.route('/patient/appointments')
def patient_appointments():
    return render_template('appointments.html')

@app.route('/patient/directory')
def patient_directory():
    return render_template('patients.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/dbms/<id>')
def dbms(id):
    if id == '1234':
        return render_template('dbms.html')

    else:
        return 'You do not have the rights to this page'

@app.route('/drop')
def drop():
    Patient.__table__.drop(engine)
    return 'droped'
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
 