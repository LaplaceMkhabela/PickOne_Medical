from flask import Blueprint
from flask import render_template,request,jsonify
from utility.nurse_utility import *

doctor_bp = Blueprint("doctor",__name__)

@doctor_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./doctor/dashboard.html',user=get_user(),analytics=get_analytics(),patients=get_appointments())

@doctor_bp.route("/patients",methods=["GET","POST"])
def patients():
    return render_template('./doctor/patients.html',user=get_user(),analytics=get_analytics(),patients=get_patients())

@doctor_bp.route("/appointments",methods=["GET"])
def appointments():
    return render_template('./doctor/appointments.html',user=get_user(),analytics=get_analytics(),appointments=get_appointments())

@doctor_bp.route("/reports",methods=["GET"])
def reports():
    return render_template('./doctor/reports.html')

@doctor_bp.route("/record",methods=["GET"])
def record():
    return render_template('./doctor/record.html',user=get_user(),analytics=get_analytics(),patients=get_appointments())

@doctor_bp.route("/update/vitals",methods=["GET","POST"])
def update_vitals():
    patient = request.get_json()
    result = vitals(patient)
    
    if result:
        return jsonify({'code':'200','msg':'Vitals updated successfully'})
    else:
        return jsonify({'code':'500','msg':'Vitals update unsuccessfull'})

