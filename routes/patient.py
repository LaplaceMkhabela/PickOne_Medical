from flask import Blueprint
from flask import render_template,request,jsonify
from database.database import Database

patient_bp = Blueprint("patient",__name__)
db = Database()

@patient_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template('./patient/dashboard.html',user=db.current_user())

@patient_bp.route("/update/profile",methods=["GET","POST"])
def update_profile():
    updated_info = request.get_json()
    
    result = db.update_patient_details(updated_info)
    
    if result:
        return jsonify({'code':'200','msg':'Information updated'})
    else:
        return jsonify({'code':'500','msg':'Sorry we could not update your profile'})