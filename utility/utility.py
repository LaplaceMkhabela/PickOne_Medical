from datetime import date,timedelta

def get_week(weekday):
    week = []
    
    for n in range(weekday,0,-1):
        week.append(date.today() - timedelta(days=n))
        
    for n in range(7 - weekday):
        week.append(date.today() + timedelta(days=n))
        
    return week

def appointment_graph_data(appointments):
    graph = {
        'x': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
        'y': []
    }
    
    for date in get_week():
        graph['y'].append(len(appointments[date]))
        
    return graph
        
def mock_graph():
    graph = {
        'x': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
        'y': [12, 19, 3, 5, 2, 3,9]
    }
    
    return graph
    
def current_date():
    return date.today()