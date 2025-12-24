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
        return redirect(url_for('dashboard',user=user))
    
    else:
        result = db.login_user(user)
    
        if result:
            if user['id'] not in session:
                session.append(user['id'])
                
            return redirect(url_for('dashboard',user=user))
        else:
            return jsonify({'code':'500','msg':'Invalid Login details'})

@app.route('/users/register',methods=['POSt','GET'])
def register():
    user = request.get_json()
    result = db.register_user(user)
    
    if result:
        return jsonify({'code':'200','msg':'Account created successfully'})
    else:
        return jsonify({'code':'500','msg':'Sorry we can\'t create your account right now'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)