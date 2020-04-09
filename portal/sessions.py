import os
from . import db

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('sessions', __name__)


@bp.route('/sessions', methods=('GET', 'POST'))
def sessions():
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM sessions AS s JOIN student_sessions AS ss ON (s.id = session_id) WHERE ss.student_id = %s;',
                (session['user'][0],))
    sessions = cur.fetchall()
    classes = []
    cur.close()

    for sess in sessions:
        course_id = sess[1]
        print(course_id)
        cur = db.get_db().cursor()
        cur.execute('SELECT name FROM courses WHERE id = %s;',
                    (sess[1],))
        classname = cur.fetchall()
        classes.append(classname[0][0])
    return render_template('portal/sessions.html', sessions=classes)


# join where session id = session id on session table
