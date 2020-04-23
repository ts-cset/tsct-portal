import os
from . import db

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__)

#------- Index -----------------------------------------------------------------
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = db.get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect email or password.'
        if error is None:
            session.clear()
            session['user'] = user
            return redirect(url_for('auth.home'))

        flash(error)

    return render_template('index.html')


#------- Home -----------------------------------------------------------------
@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('portal/home.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
