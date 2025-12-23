from flask import Flask, render_template, request,redirect,url_for,jsonify
from database.database import *
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/registration_page')
def registration_page():
    return render_template('./login_system/register.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)