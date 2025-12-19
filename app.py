from flask import Flask, render_template, request,redirect,url_for,jsonify
from database.database import *
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")