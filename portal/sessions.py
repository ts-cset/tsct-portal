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

    # grabs course id from the one clicked on
    course_id = request.args.get('course_id')

    # shows student sessions
    if session['user'][4] == 'student':
        cur.execute('SELECT * FROM sessions AS s JOIN student_sessions AS ss ON (s.id = session_id) WHERE ss.student_id = %s;',
                    (session['user'][0],))

    # shows teachers session according to which course they are looking at
    if session['user'][4] == 'teacher':
        cur.execute('SELECT * FROM sessions WHERE teacher_id = %s AND course_id = %s;',
                    (session['user'][0], course_id))

    sessions = cur.fetchall()
    classes = []
    cur.close()

    for sess in sessions:
        course_id = sess[1] # sess[1] = course id from session table
        cur = db.get_db().cursor()
        # grabbing name of the course by session's fk
        cur.execute('SELECT name FROM courses WHERE id = %s;',
                    (sess[1],))
        classname = cur.fetchall()
        # pulling string out of nested list
        classes.append(classname[0][0])

    return render_template('portal/sessions.html', sessions=classes)


# join where session id = session id on session table
