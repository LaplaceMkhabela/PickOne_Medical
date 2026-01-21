from flask import Blueprint
from flask import render_template,request,jsonify,redirect,url_for
from utility.nurse_utility import *
from utility.model import ai_summary,html_parser,ai_assistant
from database.database import Database
from database.chat_database import ChatDb

doctor_bp = Blueprint("doctor",__name__)
db = Database()
chat_db = ChatDb()

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

@doctor_bp.route("/record/<id>",methods=["GET","POST"])
def patient_record(id):
    patient = get_patient_record(str(id))
    date = list(patient['record'].keys())[-1]
    vitals = patient['record'][date]
    summary = ai_summary(patient['record'])
    summary = html_parser(summary)
    #patient_analytics = get_trends()

    return render_template('./doctor/record.html',patient=patient,vitals=vitals,summary=summary)
    
@doctor_bp.route("/view",methods=["GET","POST"])
def view_patient():
    patient = request.get_json()
    
    if patient['id'] != '':
        record = get_patient_record(patient['id'])
        
        if record:
            return jsonify({"code":"200","link":f"/doctor/record/{patient['id']}"})
        
        else:
            return jsonify({"code":"500","msg":"Failed to retrieve patient record"})
        
    else:
        return jsonify({"code":"500","msg":"Failed to retrieve patient id"})

@doctor_bp.route("/chat/<id>",methods=["GET","POST"])
def chat(id):
    history = get_patient_record(str(id))['record']
    question = request.get_json()['query']
    answer = ai_assistant(history,question)
    
    
    return jsonify({'code':'200','msg':answer})

@doctor_bp.route("/chat/load",methods=["GET","POST"])
def chat_load():
    doctor_id = db.current_user['id']
    chats = chat_db.load_chats(doctor_id)
    
    return jsonify({'code':'200','msg':chats})
    

