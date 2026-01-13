from flask import Blueprint
from flask import render_template,request,jsonify,redirect,url_for
from utility.nurse_utility import *

login_bp = Blueprint("login",__name__)

