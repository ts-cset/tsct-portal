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

    # shows student sessions
    if session['user'][4] == 'student':
        cur.execute('SELECT * FROM sessions AS s JOIN student_sessions AS ss ON (s.course_id = ss.course_id and s.section = ss.section) WHERE ss.student_id = %s;',
                    (session['user'][0],))

    # shows teachers session according to which course they are looking at
    if session['user'][4] == 'teacher':
        if(course_id == None):
            return redirect(url_for('courses.courses'))
        cur.execute('SELECT * FROM sessions WHERE teacher_id = %s AND course_id = %s;',
                    (session['user'][0], course_id))

    sessions = cur.fetchall()
    classes = []
    sections = []
    if session['user'][4] == 'student':
        course_id = []
    cur.close()

    for sess in sessions:

        cur = get_db().cursor()

        # grabbing name of the course by session's fk
        cur.execute('SELECT name FROM courses WHERE id = %s;',
                    (sess[0],))
        classname = cur.fetchall()
        if session['user'][4] == 'student':
            course_id.append(sess[0])
        # pulling string out of nested list
        classes.append(classname[0][0])
        sections.append(sess[2])
    if session['user'][4] == 'teacher':
        return render_template('portal/sessions.html', sessions=classes, sections=sections, course_id=course_id)

    if session['user'][4] == 'student':
        return render_template('portal/sessions.html', sessions=classes, sections=sections, course_id=course_id)


@bp.route('/createsession', methods=("GET", "POST"))
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
        teacher_id = session['user'][0]
        students = request.form.getlist('students')

        cur = get_db().cursor()
        cur.execute(
            """SELECT * FROM sessions WHERE course_id = %s and section = %s;""", (course_id, section))
        existingsection = cur.fetchall()
        if existingsection != []:
            error = 'Section Already Exists'
            # TODO: don't remove entered info
            session['section'] = section
            session['meeting'] = meeting_time
            session['location'] = location
            flash(error)
            return render_template('portal/createsession.html', all_students=all_students)
        cur.execute("""INSERT INTO sessions (course_id,section, meeting_time, location, teacher_id)
                        VALUES (%s, %s, %s, %s, %s);""", (course_id, section, meeting_time, location, teacher_id))
        get_db().commit()
        session['section'] = ''
        session['meeting'] = ''
        session['location'] = ''

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

    return render_template('portal/createsession.html', all_students=all_students)


# @bp.route('/<int:course_id>/<section>/editsession', methods=("GET", "POST"))
# def session_edit(course_id, section):
#     """Edits the session name/info"""
#     cur = get_db().cursor()
#     teacher = session['user'][0]
#     cur.execute("SELECT * FROM sessions WHERE section= %s AND course_id = %s;",
#                 (section, course_id))
#     selected_session = cur.fetchone()
#
#     if session['user'][4] == 'teacher':
#         return render_template('portal/home.html')
#
#     if request.method == "POST":
#         section = request.form['section']
#         meeting_time = request.form['meeting']
#         location = request.form['location']
#         teacher_id = session['user'][0]
#         students = request.form.getlist('students')
#
#         cur.execute("DELETE FROM student_sessions WHERE section = %s AND course_id = %s;",
#                     (section, course_id))
#         # Remove all students from previous sessions
#
#         cur.execute(
#             """UPDATE sessions SET (course_id,section, meeting_time, location, teacher_id) = (%s, %s, %s, %s, %s)
#                 WHERE section = %s AND course_id = %s ;""", (course_id, section, meeting_time, location, teacher_id, section, course_id)
#         )
#
#         get_db().commit()
#         cur.close()
#
#         return redirect(url_for('courses.courses'))
#
#     return render_template("portal/editsession.html", course=course)


@bp.route('/viewsession', methods=('GET', 'POST'))
def session_view():
    """View for seeing more session details."""
    cur = get_db().cursor()
    course_id = request.args.get("course_id")
    section = request.args.get("section")
    classname = request.args.get("class")

    cur.execute(
        "SELECT * FROM sessions WHERE course_id = %s AND section = %s;", (course_id, section))
    session_info = cur.fetchone()
    print(session_info)

    return render_template('portal/viewsession.html', course_id=course_id, section=section,  classname=classname, session_info=session_info)


@bp.route('/deletesession', methods=("POST",))
def session_delete():
    """View for deleting session"""
    if session['user'][4] != 'teacher':
        return render_template('portal/home.html')  # if the are a teacher
        # TODO: check teacher id
    session_info = request.form['session_to_delete']
    course_id = request.form['course_id']
    section = request.form['section']
    teacher = session['user'][0]
    cur = get_db().cursor()
    cur.execute("SELECT * FROM sessions WHERE  course_id= %s and section = %s",
                (course_id, section))
    session_information = cur.fetchone()
    if session_information['teacher_id'] != teacher:
        return render_template('portal/home.html')

    if request.method == 'POST':
        cur.execute("DELETE FROM assignments WHERE  course_id= %s and section = %s;",
                    (course_id, section))
        get_db().commit()
        cur.execute("DELETE FROM student_sessions WHERE  course_id= %s and section = %s;",
                    (course_id, section))
        get_db().commit()
        cur.execute("DELETE FROM sessions WHERE course_id = %s and section = %s;",
                    (course_id, section))
        get_db().commit()

        return redirect(url_for('courses.courses'))
    else:  # if not a teacher, send to home
        return render_template('portal/home.html')
