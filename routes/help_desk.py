from flask import Blueprint
from flask import render_template,request,jsonify,redirect,url_for
import datetime
from utility.nurse_utility import *

help_desk_bp = Blueprint("help_desk",__name__)

# Help Desk --------------------------------------------------------------------------------------------------------------
@help_desk_bp.route('/dashboard',methods=["POST","GET"])
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
            appointments = "Nothing yet"
        
        
        return render_template('./help_desk/dashboard.html',user=current_user,appointments=appointments,stats=stats,graph=mock_graph())
    
    
    url = f'{current_user['role']}/dashboard'
    return redirect(url)


@help_desk_bp.route('/appointments',methods=["POST","GET"])
def help_desk_appointments():
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
            appointments = "Nothing yet"
        
        
        return render_template('./help_desk/appointments.html',user=current_user,appointments=appointments,stats=stats)

@help_desk_bp.route('/appointments/new',methods=["POST","GET"])
def create_appointment():
    appointment = request.get_json()
    result = db.create_appointment(db.current_user(),appointment)
    
    if result:
        return jsonify({'code':'200','msg':'Appointment updated successfully'})
    else:
        return jsonify({'code':'500','msg':'Failure connecting to database'})
    