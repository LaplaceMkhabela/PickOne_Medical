from flask import Flask, render_template, request,redirect,url_for,jsonify
from database.database import *
import datetime

app = Flask(__name__)
db = Database()
session = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/registration_page')
def registration_page():
    return render_template('./login_system/register.html')

@app.route('/users/login',methods=['POSt','GET'])
def login():
    user = request.get_json()
    
    if user['id'] in session:
        return redirect(url_for('welcome_page'))
    
    else:
        result = db.login_user(user)
    
        if result:
            if user['id'] not in session:
                session.append(user['id'])
                
            return jsonify({'code':'200','link':'/users/welcome'})
        else:
            return jsonify({'code':'500','msg':'Invalid Login details'})

@app.route('/users/register',methods=['POST','GET'])
def register():
    user = request.get_json()
    result = db.register_user(user)
    
    if result:
        return jsonify({'code':'200','msg':'Account created successfully'})
    else:
        return jsonify({'code':'500','msg':'Sorry we can\'t create your account right now'})
    
@app.route('/users/welcome')
def welcome_page():
    return render_template('./welcome/welcome.html')

@app.route('/dashboard')
def dashboard():
    current_user = db.current_user()
    
    if current_user['role'] == 'help_desk':
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        appointments = db.get_appointments(current_user)
        stats = {
            "patients": 0,
            "appointments" : 0,
            "cancelled": 0
        }
        
        try:
            appointments = appointments[date]
            
            for appointment in appointments:
                if appointment['status'] == 'Confirmed':
                    stats['appointments'] = stats.get('appointments') + 1
                    
                else:
                    stats['cancelled'] = stats.get('cancelled') + 1
                
                stats['patients'] = stats.get('patients') + 1
            
        except:
            appointments = []
        
        
        return render_template('./help_desk/dashboard.html',user=current_user,appointments=appointments,stats=stats)
    
    return f'nothing yet'

@app.route('/dashboard/appointments/new',methods=["POST","GET"])
def create_appointment():
    appointment = request.get_json()
    result = db.create_appointment(db.current_user(),appointment)
    
    if result:
        return jsonify({'code':'200','msg':'Appointment updated successfully'})
    else:
        return jsonify({'code':'500','msg':'Failure connecting to database'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)