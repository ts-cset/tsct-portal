import os
from portal.db import get_db
from portal.auth import teacher_required, login_required
from portal.errorfuncs import validate_section, remove_prev_info, keep_prev_info

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('sessions', __name__)


@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
def sessions():
    cur = get_db().cursor()

    # grabs course id from the one clicked on
    course_id = request.args.get('course_id')

    # shows student sessions
    if g.user['role'] == 'student':
        cur.execute('SELECT * FROM sessions AS s JOIN student_sessions AS ss ON (s.course_id = ss.course_id and s.section = ss.section) WHERE ss.student_id = %s;',
                    (g.user['id'],))

    # shows teachers session according to which course they are looking at
    if g.user['role'] == 'teacher':
        if(course_id == None):
            return redirect(url_for('courses.courses'))
        cur.execute('SELECT * FROM sessions WHERE teacher_id = %s AND course_id = %s;',
                    (g.user['id'], course_id))

    sessions = cur.fetchall()
    classes = []
    sections = []
    if g.user['role'] == 'student':
        course_id = []
    cur.close()

    for sess in sessions:

        cur = get_db().cursor()

        # grabbing name of the course by session's fk
        cur.execute('SELECT name FROM courses WHERE id = %s;',
                    (sess[0],))
        classname = cur.fetchall()
        if g.user['role'] == 'student':
            course_id.append(sess[0])
        # pulling string out of nested list
        classes.append(classname[0][0])
        sections.append(sess[2])
    if g.user['role'] == 'teacher':
        return render_template('portal/sessions.html', sessions=classes, sections=sections, course_id=course_id)

    if g.user['role'] == 'student':
        return render_template('portal/sessions.html', sessions=classes, sections=sections, course_id=course_id)


@bp.route('/createsession', methods=("GET", "POST"))
@teacher_required
def session_create():
    """View for creating a session"""
    cur = get_db().cursor()
    course_id = request.args.get('course_id')
    # grabbing name of the course by session's fk

    # ---join for grabbing enrolled_students---
    # cur.execute('SELECT * FROM student_sessions JOIN users ON student_id =users.id  WHERE session_id = %s;',
    #             (1,))
    # enrolled_students = cur.fetchall()
    cur.execute('SELECT * FROM users WHERE role = %s;', ('student',))
    all_students = cur.fetchall()

    if request.method == "POST":

        section = request.form['section']
        meeting_time = request.form['meeting']
        location = request.form['location']
        teacher_id = g.user['id']
        students = request.form.getlist('students')

        cur = get_db().cursor()
        check = validate_section(course_id, section, meeting_time, location, all_students)
        if check == True:
            cur.execute("""INSERT INTO sessions (course_id,section, meeting_time, location, teacher_id)
                            VALUES (%s, %s, %s, %s, %s);""", (course_id, section, meeting_time, location, teacher_id))
            get_db().commit()
            remove_prev_info('section')

            for student in students:
                # find student in user db then grab it by name
                cur = get_db().cursor()
                cur.execute('SELECT * FROM users WHERE name = %s;', (student,))
                student_info = cur.fetchone()
                student_id = student_info[0]
                # create a new session for each student
                cur.execute("""INSERT INTO student_sessions (course_id, section, student_id)
                                        VALUES (%s, %s, %s);""", (course_id, section, student_id))
                get_db().commit()
                cur.close()

            return redirect(url_for('courses.courses'))
        else:
            return check

    return render_template('portal/createsession.html', all_students=all_students)


@bp.route('/viewsession', methods=('GET', 'POST'))
@login_required
def session_view():
    """View for seeing more session details."""
    cur = get_db().cursor()
    course_id = request.args.get("course_id")
    section = request.args.get("section")
    classname = request.args.get("class")

    cur.execute(
        "SELECT * FROM sessions WHERE course_id = %s AND section = %s;", (course_id, section))
    session_info = cur.fetchone()

    return render_template('portal/viewsession.html', course_id=course_id, section=section,  classname=classname, session_info=session_info)


@bp.route('/deletesession', methods=("POST",))
@teacher_required
def session_delete():
    """View for deleting session"""
    course_id = request.form['course_id']
    section = request.form['section']
    teacher = g.user['id']
    cur = get_db().cursor()
    cur.execute("SELECT * FROM sessions WHERE  course_id= %s and section = %s",
                (course_id, section))
    session_information = cur.fetchone()
    if session_information['teacher_id'] != teacher:
        return redirect(url_for('sessions.sessions'))

    if request.method == 'POST':
        cur.execute("SELECT * FROM assignments WHERE course_id= %s AND section = %s;",
                    (course_id, section))
        selected = cur.fetchall()
        print(section)
        print(course_id)
        print(selected)
        cur.execute("DELETE FROM sessions WHERE course_id = %s AND section = %s;",
                    (course_id, section))
        get_db().commit()

        return redirect(url_for('courses.courses'))
