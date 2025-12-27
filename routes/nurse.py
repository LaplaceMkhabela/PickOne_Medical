from flask import Blueprint
from flask import render_template
from database.database import Database

nurse_bp = Blueprint("nurse",__name__)
db = Database()
current_user = db.current_user()

@nurse_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./nurse/dashboard.html',user=current_user)

@nurse_bp.route("/patients",methods=["GET"])
def patients():
    patients_list = db.get_patients()
    return render_template('./nurse/patients.html')

@nurse_bp.route("/appointments",methods=["GET"])
def appointments():
    appointments_data = db.get_appointments({'role':'help_desk'})
    appointments_list = []
    
    for date,appointment in appointments_data.items():
        appointments_list.append(appointment)
        
    return render_template('./nurse/appointments.html',appointments=appointments_list)

@nurse_bp.route("/reports",methods=["GET"])
def reports():
    return render_template('./nurse/reports.html')