import os
from portal.db import get_db

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('sessions', __name__)


@bp.route('/sessions', methods=('GET', 'POST'))
def sessions():
    cur = get_db().cursor()

    # grabs course id from the one clicked on
    course_id = request.args.get('course_id')
    print(course_id)

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
        cur = get_db().cursor()
        # grabbing name of the course by session's fk
        cur.execute('SELECT name FROM courses WHERE id = %s;',
                    (sess[1],))
        classname = cur.fetchall()
        # pulling string out of nested list
        classes.append(classname[0][0])

    return render_template('portal/sessions.html', sessions=classes, course_id=course_id)

@bp.route('/createsession', methods=("GET", "POST"))
def session_create():
    """View for creating a session"""
    course_id = request.args.get('course_id')

    if request.method == "POST":
        section = request.form['section']
        meeting_time = request.form['meeting']
        location = request.form['location']
        teacher_id = session['user'][0]

        # make a query that inserts into courses table with this info and teacher id
        cur = get_db().cursor()

        cur.execute("""INSERT INTO sessions (course_id,section, meeting_time, location, teacher_id)
                        VALUES (%s, %s, %s, %s, %s);""", (course_id, section, meeting_time, location, teacher_id))
        get_db().commit()
        cur.close()

        return redirect(url_for('courses.courses'))

    return render_template('portal/createsession.html')