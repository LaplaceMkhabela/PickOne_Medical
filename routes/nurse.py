from flask import Blueprint
from flask import render_template

nurse_bp = Blueprint("nurse",__name__)

@nurse_bp.route("/nurse/dashboard",methods=["GET"])
def dashboard():
    return render_template('./nurse/dashboard.html')