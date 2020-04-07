import os

from . import db

from portal.db import get_db
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(generate_password_hash(password))
        cur = db.get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        if user is None:
            print('incorrect email')
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            print('incorrect password')
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user'] = user
            print(session['user']['role'])
            return render_template('portal/home.html')

        flash(error)

    return render_template('index.html')
