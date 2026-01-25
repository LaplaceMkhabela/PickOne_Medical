from flask import Blueprint
from flask import render_template,request,jsonify
from database.database import Database

patient_bp = Blueprint("patient",__name__)
db = Database()

@patient_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./patient/dashboard.html',user=db.current_user())