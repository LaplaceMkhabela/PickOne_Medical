import csv
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login/<type>/<id>/<key>')
def login(type, id, key):

    # Collecting all users from the CSV file
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Authenticating the user
        if [type, id, key] in reader:
            return json.dumps({'status': 'yes', 'access': 'granted'})
        else:
            return json.dumps({'status': 'no', 'access': 'denied'})
            

@app.route('/register/<type>/<id>/<key>/<name>/<surname>/<email>')
def register(type, id, key, name, surname, email):

    # Collecting all users from the CSV file
    with open('users.csv', 'a+', newline='') as file:
        file.seek(0)
        reader = list(csv.reader(file))
        
        new_user = [type, id, key, name, surname, email]

        # Checking if the user is not already registered.
        if new_user in reader:
            return json.dumps({'status': 'no', 'access': 'denied'})
        else:
        

if __name__ == '__main__':
    app.run(debug=True)