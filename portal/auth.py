import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        cur = db.get_db().cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        cur.close()

        if user is None:
            error = 'Incorrect email or password'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect email or password'


        if error is None:
            session.clear()
            session['users_id'] = user['id']
            return redirect(url_for('portal.userpage'))
        flash(error)


    return render_template('account/login.html')

@bp.before_app_request
def load_logged_in_users():
    users_id = session.get('users_id')
    cur = db.get_db().cursor()

    if users_id is None:
        g.users = None
    else:
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (users_id,)
        )
        g.users = cur.fetchone()
        cur.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.users is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def teacher_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.users['role'] != 'teacher':
            error = "Not authorized"
            return render_template('error.html', error=error)

        return view(**kwargs)

    return wrapped_view
