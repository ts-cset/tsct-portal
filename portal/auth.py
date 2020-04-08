import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
bp = Blueprint("auth", __name__)


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()

        if user is None:
            error = 'Incorrect credentials.'
        elif not user['password'] == password:
            error = 'Incorrect credentials.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if session['user_id'] == user['id'] and user['role'] == 'student':
                return redirect(url_for('college.student'))
            elif session['user_id'] == user['id'] and user['role'] == 'teacher':
                return redirect(url_for('college.home'))

        cur.close()
        flash(error)

    return render_template('index.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    cur = db.get_db().cursor()

    if user_id is None:
        g.user = None
    else:
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
