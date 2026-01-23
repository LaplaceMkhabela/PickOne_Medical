import os
import json


class ChatDb:
    def __init__(self):
        os.makedirs('database/database_files/chats', exist_ok=True)
        self.chats_path = os.path.join(
            'database', 'database_files', 'chats', 'chats.json')

        if not os.path.exists(self.chats_path):
            with open(self.chats_path, 'x') as file:
                file.write(json.dumps({"chats": {}}))
                print('created chats.json')

    def save(self, doctor_id, patient_id, question, response):
        data = self.read_data()
        data['chats'][doctor_id][patient_id].append((question,response))
        print(data['chats'])
        self.write_data(data)
        # try:
        #     data['chats'][doctor_id][patient_id].append(question, response)
        #     self.write_data(data)
        # except:
        #     raise ValueError('Failed to save chats')

    def read_data(self):
        with open(self.chats_path, 'r') as file:
            try:
                data = json.loads(file.read())
                return data

            except:
                raise ValueError('Could not open chats file at:')

    def write_data(self, data):
        with open(self.chats_path, 'w') as file:
            try:
                file.write(json.dumps(data))

                return True

            except:
                raise ValueError('Could not save chats file')

    def load_chats(self, doctor_id, patient_id):
        data = self.read_data()

        try:
            chats = data['chats'][doctor_id][patient_id]
            return chats

        except KeyError:
            data['chats'].update({doctor_id: {patient_id: []}})
            self.write_data(data)
            return []
