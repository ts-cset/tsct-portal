from flask import Flask, render_template, Blueprint

bp = Blueprint("portal", __name__)

@bp.route('/')
def index():
    return render_template('index.html')
@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/student")
def student():
    return render_template("student-home.html")
