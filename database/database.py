import os
import json
from pwdlib import PasswordHash

class Database:
    def __init__(self):
        self.encoder = PasswordHash.recommended()
        self.user = {}
        self.patient_path = os.path.join('database','database_files','patient','patient_db.json')
        self.help_desk_path = os.path.join('database','database_files','help_desk','help_desk_db.json')
        self.nurse_path = os.path.join('database','database_files','nurse','nurse_db.json')
        self.doctor_path = os.path.join('database','database_files','doctor','doctor_db.json')
        self.initialise_files()
        self.paths = {
            'patient':os.path.join('database','database_files','patient','patient_db.json'),
            'doctor':os.path.join('database','database_files','doctor','doctor_db.json'),
            'nurse': os.path.join('database','database_files','nurse','nurse_db.json'),
            'help_desk':os.path.join('database','database_files','help_desk','help_desk_db.json')
        }
        
    def initialise_files(self):
        os.makedirs('database/database_files/patient',exist_ok=True)
        os.makedirs('database/database_files/help_desk',exist_ok=True)
        os.makedirs('database/database_files/nurse',exist_ok=True)
        os.makedirs('database/database_files/doctor',exist_ok=True)
        
        for path in [(self.patient_path,'patient'),(self.help_desk_path,'help_desk'),(self.nurse_path,'nurse'),(self.doctor_path,'doctor')]:
            if not os.path.exists(path[0]):
                with open(path[0],'w') as file:
                    file.write(json.dumps({path[1]:{
                        "ids":[],
                        "accounts":{},
                        "appointments":{}
                    }}))
        
         
    def login_user(self,current_user):
        path = os.path.join('database','database_files',f'{current_user['role']}',f'{current_user['role']}_db.json')
        user_data = self.read_db(path)
        user_account = user_data[current_user['role']]['accounts'][current_user['id']]
            
        if user_account['id'] == current_user['id'] and self.encoder.verify(current_user['password'],user_account['password']):
                self.user = user_account
                return True
                
        return False
    
    def register_user(self,current_user):
        path = os.path.join('database','database_files',f'{current_user['role']}',f'{current_user['role']}_db.json')
        user_data = self.read_db(path)
        user_ids = user_data[current_user['role']]['ids']
            
        if current_user['id'] in user_ids:
            return False
        else:
            current_user['password'] = self.encoder.hash(current_user['password'])
            user_data[current_user['role']]['accounts'].update({current_user['id']:current_user})
            user_data[current_user['role']]['ids'].append(current_user['id'])
            self.write_db(path,user_data)
            return True
    
    def create_appointment(self,user,appointment):
        vitals = {
        'status': 'Confirmed',
        'bp':'None',
        'weight': 'None',
        'temp': 'None'
        }
        appointment.update(vitals)
        
        try:
            db = self.read_db(self.help_desk_path)
            appointments = db[user['role']]['appointments']
            
            if appointment['date'] in appointments.keys():
                appointments[appointment['date']].append(appointment)
                
            else:
                appointments.update({appointment['date']:[]})
                appointments[appointment['date']].append(appointment)
            
            self.write_db(self.help_desk_path,db)
            
            return True
            
        except:
            return False
        
    def create_session(self,user):
        accounts = self.read_db(self.paths[user['role']])[user['role']]['accounts']
        
        for account in accounts:
            if user['id'] == account['id']:
                current_user = account
        try:
            with open(os.path.join(os.getcwd(),'database','database_files','sessions','sessions.json'),'w') as file:
                file.write(json.dumps({"current_user": current_user}))
                
        except:
            raise ValueError('Failed to create session')
        
    def get_appointments(self,user):
        appointments = self.read_data()[user['role']]
        return appointments['appointments']
    
    def get_patients(self):
        #patients = self.read_db(self.patient_records_path)['patient']
        patients = self.read_db(self.patient_path)['patient']
        return patients['accounts']
        
    def current_user(self):
        try:
            with open(os.path.join(os.getcwd(),'database','database_files','sessions','sessions.json'),'r') as file:
                session = json.loads(file.read())
                self.user = session['current_user']
                
        except:
            raise ValueError('Failed to create session')
        
        return self.user
    
    def update_patient_file(self,id,date,new_record):
        data = self.read_db(self.patient_records_path)
        
        try:
            data['patient'][id]['record'][date].update(new_record)
            self.write_db(self.patient_records_path,data)
            
        except KeyError:
            data['patient'][id].update({'record':{date:new_record}})
            self.write_db(self.patient_records_path,data)
            
    def update_patient_details(self,info):
        data = self.read_db(self.patient_records_path)
        
        data['patient']['accounts'][info['id']].update({
            "name":info['name'],
            "email": info['email'],
            "dob": info['dob'],
            "gender": info['gender'],
            "phone": info['phone'],
            "address": info['address'],  
        })
        
    
             
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
        
    def read_db(self,path):
        with open(path,'r') as file:
            try:
                db = json.loads(file.read())
                return db
            except:
                raise "Failed to read db"   
            
    def write_db(self,path,data):
        with open(path,'w') as file:
            try:
                file.write(json.dumps(data))
                return True
            except:
                return False
        
            
    
                
            
            
            