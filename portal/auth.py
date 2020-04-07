from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db

bp = Blueprint("auth", __name__)

@bp.route('/login', methods=('GET', 'POST'))
def login():

    return render_template('login.html')
