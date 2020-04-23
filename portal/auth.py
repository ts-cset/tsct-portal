import os
from . import db
import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__)

@bp.before_app_request
def load_logged_in_user(): # transfers session user id to safer g object
    user_id = session.get('user_id')
    cur = db.get_db().cursor()
    if user_id is None:
        g.user = None
    else:
        cur.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
        g.user = cur.fetchone() # g has all information from users table for that user id

def login_required(view): # requires the user to be logged in
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.index')) # if not logged, redirect them to the login page

        return view(**kwargs)

    return wrapped_view

def teacher_required(view): # requires the user to have the role of teacher
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: # if not logged in, go to login
            return redirect(url_for('auth.index'))
        if g.user['role'] != 'teacher': # if not a teacher, redirect to home page.
            return redirect(url_for('auth.home'))

        return view(**kwargs)

    return wrapped_view

#------- Index -----------------------------------------------------------------
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = db.get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s;', (email,)
        )
        user = cur.fetchone()
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect email or password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
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
