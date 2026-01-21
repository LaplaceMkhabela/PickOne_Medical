import os
import json

class ChatDb:
    def save(self,doctor_id,question,response):
        with open(os.path.join(os.getcwd(),'database','database_files','users.json'),'w') as file:
            try:
                data = self.read_data()
                
                try:
                    for id,chats_list in data['doctor']['chats'].items():
                    
                        if id == doctor_id:
                            chats_list.append(question)
                            chats_list.append(response)
                except:
                    data = self.read_data()
                    
                    chats = data['doctor']['chats']
                    chats.update({str(doctor_id):[question,response]})
                    
            except:
                raise ValueError('Failed to open chats')
                               
                
    def read_data(self):
        with open(os.path.join(os.getcwd(),'database','database_files','users.json'),'r') as file:
            try:
                data = json.loads(file.read())
                
                return data 
            
            except:
                raise ValueError('Could not open file')
            
    def load_chats(self,id_doctor):
        try:
            data = self.read_data()
            
            try:
                for id,chats_list in data['doctor']['chats'].items():
                    if id == id_doctor:
                        return chats_list
                    
            except:
                return ('Failed to load chats')
            
                
        except:
            return ('failed to read chats database')
        