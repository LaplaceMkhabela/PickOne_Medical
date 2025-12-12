from flask import Flask, render_template, request
import sqlite3 

db = SQLAlchemy(app)

app = Flask(__name__)
@app.route("/")
def index():
    patient = get
    

    return render_template("/home.html")