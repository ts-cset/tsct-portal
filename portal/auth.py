from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools
from . import db

bp = Blueprint("auth", __name__)

@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':

        con = db.get_db()
        cur = con.cursor()

        email = request.form['email']
        password = request.form['password']

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        error = None

        if not email:
            print('no email')
            error = 'Enter an email'

        elif not password:
            print('no password')
            error = 'Enter a password'

        elif not user or user['password'] != password:
            error = 'Incorrect email or password'

        if error == None:

            session.clear()
            session['user_id'] = user['id']

            cur.close()
            con.close()

            return redirect('/')

        cur.close()
        con.close()

        flash(error)

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.before_app_request
def load_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
                g.user = cur.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect('/login')

        return view(**kwargs)

    return wrapped
