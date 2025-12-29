from flask import Blueprint
from flask import render_template,request,jsonify
from utility.nurse_utility import *

nurse_bp = Blueprint("nurse",__name__)

@nurse_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./nurse/dashboard.html',user=get_user(),analytics=get_analytics(),patients=get_appointments())

@nurse_bp.route("/patients",methods=["GET","POST"])
def patients():
    return render_template('./nurse/patients.html',user=get_user(),analytics=get_analytics(),patients=get_appointments())

@nurse_bp.route("/appointments",methods=["GET"])
def appointments():
    return render_template('./nurse/appointments.html',user=get_user(),analytics=get_analytics(),appointments=get_appointments())

@nurse_bp.route("/reports",methods=["GET"])
def reports():
    return render_template('./nurse/reports.html')

@nurse_bp.route("/update/vitals",methods=["GET","POST"])
def reports():
    patient = request.get_json()
    result = update_vitals(patient)
    
    if result:
        return jsonify({'code':'200','msg':'Vitals updated successfully'})
    else:
        return jsonify({'code':'500','msg':'Vitals update unsuccessfull'})

