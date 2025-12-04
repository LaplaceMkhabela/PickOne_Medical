import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login/<type>/<id>/<key>')
def login(type, id, key):

    # Collecting all users from the CSV file
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Authenticating the user
        if type.lower() == 'patient':# If the user is a patient
            if [type, id, key] in reader:
                return render_template('home.html', user=[type, id, key])
            else:
                return render_template('login.html')
            
        elif type.lower() == 'doctor':# If the user is a doctor
            if [type, id, key] in reader:
                return render_template('home.html', user=[type, id, key])
            else:
                return render_template('login.html')
            


@app.route('/register/<type>/<id>/<key>')
def register(type, id, key):

    # Collecting all users from the CSV file
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Authenticating the user
        if [type, id, key] in reader:
            # If the user is already registered
            return render_template('home.html', user=[type, id, key])
        
        else:
            return render_template('login.html')
        

if __name__ == '__main__':
    app.run(debug=True)