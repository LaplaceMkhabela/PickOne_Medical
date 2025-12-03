from flask import Flask, render_template,request
from utility.database import *
import json
app = Flask(__name__)


@app.route('/')
def index():
    return 'hello doctor'

@app.route('/view')
def view():
    # u = create_user(db, "Michael", "michael@example.com")
    # print(u.id, u.name)
    u = get_user(db,'1')
    print(u)
    # return f'{u.id} - {u.name}'
    return f'g-{u.name}'

@app.route('/doctor/<hpsa_id>')
def doctor_page(hpsa_id):
    return f'Welcome doctor {hpsa_id}'

@app.route('/patient/<patient_id>')
def patient_page(patient_id):
    return f'Welcome patient {patient_id}'

@app.route('/search/<id>')
def search_patiennt(id):
    patient = get_user(db,str(id))

    card = {
        'id': patient.id,
        'name':patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'bp': patient.bp,
        'weight': patient.weight,
        'bmi': patient.bmi,
        'temp': patient.temp,
        'pulse': patient.pulse,
        'bpm' : patient.bpm

    }

    results = json.dumps(card)

    return results

@app.route('/patient_profile/<id>')
def patient_profile(id):
    return render_template('expression')

@app.route('/diagnosis',methods=['GET','POST'])
def diagnosis():
    if request.method == 'POST':
        # Retrieve form data using request.form
        # Use .get() to avoid a KeyError if the field is missing, optionally providing a default value
        diagnosis = request.form.get('diagnosis')
        treatment = request.form.get('treatment')
    return render_template('expression')



if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    card = {
        'name':'tesla',
        'email': 'tesl@tesla.com',
        'phone': '078 6765 786',
        'age': '127',
        'gender': 'male',
        'bp': '122/71',
        'weight': '78',
        'bmi': '89',
        'temp': '78',
        'pulse': '70',
        'bpm' : '60'

    }

    u = create_user(db,card['name'],card['email'],card['phone'],card['age'],card['gender'],card['bp'],card['weight'],card['bmi'],card['temp'],card['pulse'],card['bpm'])
    app.run(host='127.0.0.1', port=5000, debug=True)
 