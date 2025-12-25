from flask import Flask, render_template, request,redirect,url_for,jsonify
from database.database import *
import datetime

app = Flask(__name__)
db = Database()
session = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/registration_page')
def registration_page():
    return render_template('./login_system/register.html')

@app.route('/users/login',methods=['POSt','GET'])
def login():
    user = request.get_json()
    
    if user['id'] in session:
        return redirect(url_for('welcome_page'))
    
    else:
        result = db.login_user(user)
    
        if result:
            if user['id'] not in session:
                session.append(user['id'])
                
            return jsonify({'code':'200','link':'/users/welcome'})
        else:
            return jsonify({'code':'500','msg':'Invalid Login details'})

@app.route('/users/register',methods=['POST','GET'])
def register():
    user = request.get_json()
    result = db.register_user(user)
    
    if result:
        return jsonify({'code':'200','msg':'Account created successfully'})
    else:
        return jsonify({'code':'500','msg':'Sorry we can\'t create your account right now'})
    
@app.route('/users/welcome')
def welcome_page():
    return render_template('./welcome/welcome.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)