from database.database import Database

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
    
    for date,appointment in appointments_data.items():
        appointments_list.extend(appointment)
        
    return appointments_list


def get_patients():
    return db.get_patients()