from flask import Blueprint
from flask import render_template

nurse_bp = Blueprint("nurse",__name__)

@nurse_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./nurse/dashboard.html')

@nurse_bp.route("/patients",methods=["GET"])
def patients():
    return render_template('./nurse/patients.html')

@nurse_bp.route("/appointments",methods=["GET"])
def appointments():
    return render_template('./nurse/appointments.html')