from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('sessions', __name__, url_prefix='/portal/sessions')

@bp.route('/<course_id>/view-session/<session_id>', methods=('GET', 'POST'))
@login_required
def view_session(course_id, session_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM session
                   WHERE id = %s;""",
                   (session_id,))
    sessions = cur.fetchall()

    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE session_id = %s;""",
                   (session_id,))
    assignments = cur.fetchall()

    cur.execute("""SELECT * FROM roster
                   WHERE session_id = %s;""",
                   (session_id,))
    rosters = cur.fetchall()
    cur.close()
    return render_template('portal/courses/sessions/view-session.html', courses=courses, sessions=sessions, rosters=rosters, assignments=assignments)

@bp.route('/<course_id>/create-session', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_session(course_id):

    if request.method == 'POST':
        name = request.form['name']
        times = request.form['times']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM session
        WHERE name = %s and courses_id = %s;
        """,
        (name, course_id))
        session = cur.fetchone()

        if session != None:
            error = "That session already exists"
            return render_template('error.html', error=error)

        if error is None:
            try:
                cur.execute("""INSERT INTO session (courses_id, times, name)
                VALUES (%s, %s, %s);
                 """,
                 (course_id, times, name))
                db.get_db().commit()
            except:
                error = "There was a problem creating that session"
                return render_template('error.html', error=error)
            else:
                cur.execute("""SELECT id FROM session
                WHERE name = %s and courses_id = %s;
                """,
                (name, course_id))
                sessions = cur.fetchone()
                session_id = sessions[0]

            return redirect(url_for('sessions.view_session', session_id=session_id, course_id=course_id))
        else:
            return redirect(url_for('sessions.create_session', course_id=course_id))
    return render_template('portal/courses/sessions/create-session.html')

@bp.route('/<course_id>/<session_id>/add-student', methods=('GET', 'POST'))
@login_required
@teacher_required
def add_student(course_id, session_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT users.*, roster.* FROM roster
                JOIN users ON users.id = roster.users_id
                WHERE session_id = %s""",
                (session_id,))
    added_students = cur.fetchall()
    cur.execute("""SELECT * FROM users
                WHERE role = 'student'""")
    all_students = cur.fetchall()

    if request.method == 'POST':
        student = request.form['student']
        error = None
        for added_student in added_students:
            print(added_student['users_id'])
            print(student)
            if added_student['users_id'] == int(student):
                error = "That student is already in the session"
                return render_template('error.html', error=error)
        try:
            cur.execute("""INSERT INTO roster (users_id, session_id)
            VALUES (%s, %s);
             """,
             (student, session_id))
            db.get_db().commit()
            cur.close()
        except:
            error = "There was a problem adding that student"
            return render_template('error.html', error=error)
        else:
            return redirect(url_for('sessions.view_session', session_id=session_id, course_id=course_id))
    return render_template('portal/courses/sessions/add-students.html', added_students=added_students, all_students=all_students)

@bp.route('/<path:subpath>/')
@login_required
def session_error(subpath=None):
    error = "404 Not found"
    return render_template('error.html', error=error)
