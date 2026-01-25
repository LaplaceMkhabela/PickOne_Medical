from flask import Flask, render_template, request,redirect,url_for,jsonify
from database.database import *
from utility.utility import *
from routes.nurse import nurse_bp
from routes.doctor import doctor_bp
from routes.users import users_bp
from routes.help_desk import help_desk_bp
from routes.patient import patient_bp
import datetime


db = Database()
session = []

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(nurse_bp,url_prefix='/nurse')
    app.register_blueprint(doctor_bp,url_prefix='/doctor')
    app.register_blueprint(users_bp,url_prefix='/users')
    app.register_blueprint(help_desk_bp,url_prefix='/help_desk')
    app.register_blueprint(patient_bp,url_prefix='/patient')
    
    return app

app = create_app()

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/error')
def error():
    return render_template('./base/error.html')




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)