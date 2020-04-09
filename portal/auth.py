import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from portal.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        cur.close()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        #If no error occurs then a user has logged in
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            #Return different views for a teacher vs student
            if user['role'] == 'teacher':
                return "Hello teacher"
                #return redirect(url_for('portal.teacher_page'))
            elif user['role'] == 'student':
                # return "hello student"
                return redirect(url_for('student.home'))

        flash(error)

    return render_template('index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))

#add this to a bp to make login required before going to a view
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view
