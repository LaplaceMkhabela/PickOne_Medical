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
    return db.get_patients()

def process_appointments(appointment_list):
    current_date = date.today()
    appointment_list = appointment_list
    
    for appointment in appointment_list:
        year,month,day = appointment['date'].split('-')
        
        if date(int(year),int(month),int(day)) > current_date:
            appointment['status'] = 'Pending'
            
        elif date(int(year),int(month),int(day)) < current_date:
            appointment['status'] = 'Cancelled'
            
        else:
            appointment['status'] = 'Confirmed'
            
    return appointment_list