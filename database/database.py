import os
import json
from pwdlib import PasswordHash

class Database:
    def __init__(self):
        self.encoder = PasswordHash.recommended()
        self.user = {}
        
    def login_user(self,current_user):
        user_data = self.read_data()
        user_accounts = user_data[current_user['role']]['accounts']
            
        for user in user_accounts:
            if user['id'] == current_user['id'] and self.encoder.verify(current_user['password'],user['password']):
                self.user = user
                return True
                
        return False
    
    def register_user(self,current_user):
        user_data = self.read_data()
        user_ids = user_data[current_user['role']]['ids']
            
        if current_user['id'] in user_ids:
            return False
        else:
            current_user['password'] = self.encoder.hash(current_user['password'])
            user_data[current_user['role']]['accounts'].append(current_user)
            user_data[current_user['role']]['ids'].append(current_user['id'])
            self.write_data(user_data)
            return True
    
    def create_appointment(self,user,appointment):
        appointment.update({'status':'Confirmed'})
        try:
            db = self.read_data()
            appointments = db[user['role']]['appointments']
            
            if appointment['date'] in appointments.keys():
                appointments[appointment['date']].append(appointment)
                
            else:
                appointments.update({appointment['date']:[]})
                appointments[appointment['date']].append(appointment)
            
            self.write_data(db)
            
            return True
            
        except:
            return False
        
    def create_session(self,user):
        try:
            with open(os.path.join(os.getcwd(),'database','database_files','sessions','sessions.json'),'w') as file:
                file.write(json.dumps({"current_user": user}))
                
        except:
            raise ValueError('Failed to create session')
        
    def get_appointments(self,user):
        appointments = self.read_data()[user['role']]
        return appointments['appointments']
    
    def get_patients(self,user):
        patients = self.read_data()[user['role']]
        return patients['accounts']
        
    def current_user(self):
        try:
            with open(os.path.join(os.getcwd(),'database','database_files','sessions','sessions.json'),'r') as file:
                session = json.loads(file.read())
                self.user = session['current_user']
                
        except:
            raise ValueError('Failed to create session')
        
        return self.user
            
                
    def write_data(self,data):
        with open(os.path.join(os.getcwd(),'database','database_files','users.json'),'w') as file:
            try:
                file.write(json.dumps(data))
                return True
            except:
                return False
            
    def read_data(self):
        with open(os.path.join(os.getcwd(),'database','database_files','users.json'),'r') as file:
            try:
                user_data = json.loads(file.read())
                return user_data
            except:
                return False
            
    
                
            
            
            