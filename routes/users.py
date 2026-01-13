from flask import Blueprint
from flask import render_template,request,jsonify,redirect,url_for
from utility.nurse_utility import *

users_bp = Blueprint("users",__name__)
session = []


@users_bp.route('/login/page')
def login_page():
    return render_template('./login_system/login.html')

@users_bp.route('/registration/page')
def registration_page():
    return render_template('./login_system/register.html')

@users_bp.route('/users/login',methods=['POSt','GET'])
def login():
    user = request.get_json()
    
    if user['id'] in session:
        return redirect(url_for('welcome_page'))
    
    else:
        result = db.login_user(user)
    
        if result:
            if user['id'] not in session:
                session.append(user['id'])
                
            db.create_session(user)
                
            return jsonify({'code':'200','link':'/users/welcome'})
        else:
            return jsonify({'code':'500','msg':'Invalid Login details'})

@users_bp.route('/users/register',methods=['POST','GET'])
def register():
    user = request.get_json()
    result = db.register_user(user)
    
    if result:
        return jsonify({'code':'200','msg':'Account created successfully'})
    else:
        return jsonify({'code':'500','msg':'Sorry we can\'t create your account right now'})
    
@users_bp.route('/users/welcome')
def welcome_page():
    return render_template('./welcome/welcome.html')

@users_bp.route('/users/logout')
def logout():
    session.remove(db.current_user()['id'])
    
    return render_template('./welcome/logout.html')
