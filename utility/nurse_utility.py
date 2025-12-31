from database.database import Database
from datetime import date
db = Database()

def get_analytics():
    appointments = db.get_appointments({'role':'help_desk'}).values()
    stats = {
        "patients": 0,
        "appointments": 0,
        "reports": 0
    }
    
    stats['patients'] = len(appointments)
    
    for appointment_list in appointments:
        for appointment in appointment_list:
            if appointment['status'] == 'Confirmed':
                stats['appointments'] = stats.get('appointments') + 1
        
    
    return stats

def get_user():
    return db.current_user()

def get_appointments():
    appointments_data = db.get_appointments({'role':'help_desk'})
    appointments_list = []
    
    for appointment in appointments_data.values():
        appointments_list.extend(appointment)
        
    return process_appointments(appointments_list)


def get_patients():
    patients = db.read_data()['patient']['accounts']
    return patients

def process_appointments(appointment_list):
    current_date = date.today()
    appointment_list = appointment_list
    
    for appointment in appointment_list:
        year,month,day = appointment['date'].split('-')
        
        if date(int(year),int(month),int(day)) > current_date:
            appointment['status'] = 'Pending'
            appointment.update({'class':'status Pending'})
            
        elif date(int(year),int(month),int(day)) < current_date:
            appointment['status'] = 'Cancelled'
            appointment.update({'class':'status Cancelled'})
            
        else:
            appointment['status'] = 'Confirmed'
            appointment.update({'class':'status Confirmed'})
            
    return appointment_list

def vitals(patient):
    data = db.read_data()
    
    try:
        for appointments in data['help_desk']['appointments'].values():
            for p in appointments:
                if p['id'] == patient['id']:
                    p['weight'] = patient['weight']
                    p['bp'] = f"{patient['bp_systolic']} / {patient['bp_diastolic']}"
                    p['temp'] = patient['temp']
                
        db.write_data(data)
        
        return True
    except:
        return False

def get_patient_record(id):
    try:
        accounts = db.read_data()['patient']['accounts']
    
        for patient in accounts:
            if patient['id'] == str(id):
                return patient
    except:
        return False
    