from flask import Blueprint
from flask import render_template,request,jsonify
from database.database import Database
from utility.utility import recent_vitals,recent_visits

patient_bp = Blueprint("patient",__name__)
db = Database()

@patient_bp.route("/dashboard",methods=["GET"])
def dashboard():
    id = db.current_user()['id']
    vitals = recent_vitals(id)
    visits = recent_visits(id)
    return render_template('./patient/dashboard.html',user=db.current_user(),vitals=vitals,visits=visits)

@patient_bp.route("/update/profile",methods=["GET","POST"])
def update_profile():
    updated_info = request.get_json()
    
    result = db.update_patient_details(updated_info)
    
    if result:
        return jsonify({'code':'200','msg':'Information updated'})
    else:
        return jsonify({'code':'500','msg':'Sorry we could not update your profile'})