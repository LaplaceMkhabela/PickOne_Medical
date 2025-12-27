from database.database import Database

db = Database()

def get_analytics():
    appointments = get_appointments()
    stats = {
        "patients": 0,
        "appointments": 0,
        "reports": 0
    }
    
    stats['patients'] = len(appointments)
    
    for appointment in appointments:
        if appointment['status'] == 'Confirmed':
            stats['appointments'] = stats.get('appointments') + 1
    
    return stats

def get_user():
    return db.current_user()

def get_appointments():
    appointments_data = db.get_appointments({'role':'help_desk'})
    appointments_list = []
    
    for date,appointment in appointments_data.items():
        appointments_list.append(appointment)
        
    return appointments_list


def get_patients():
    patients_list = db.get_patients()
    pass