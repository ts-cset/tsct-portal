from flask import Flask, render_template, g, redirect, url_for, Blueprint, request

from . import db

import datetime

bp = Blueprint("college", __name__)

@bp.route('/')
def index():
    return render_template('index.html')
@bp.route("/home")
def home():
    return render_template("home.html")
