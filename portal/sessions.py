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
    cur.execute("""SELECT * FROM roster
                   WHERE session_id = %s;""",
                   (session_id,))
    rosters = cur.fetchall()
    cur.close()
    return render_template('portal/courses/sessions/view-session.html', courses=courses, sessions=sessions, rosters=rosters)

@bp.route('/<course_id>/create-session', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_session(course_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM users
                   WHERE role = 'student'""")
    students = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        name = request.form['name']
        times = request.form['times']
        students = request.form.getlist('students')
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

        if error is None:
            cur.execute("""INSERT INTO session (courses_id, times, name)
            VALUES (%s, %s, %s);
             """,
             (course_id, times, name))
            db.get_db().commit()
            cur.execute("""SELECT id FROM session
                           WHERE courses_id = %s and name = %s and times = %s""",
                           (course_id, name, times))
            session = cur.fetchone()

            for student in students:
                cur.execute("""INSERT INTO roster (users_id, session_id)
                VALUES (%s, %s);
                 """,
                 (student, session[0]))
                db.get_db().commit()
            cur.close()
            return redirect(url_for('portal.userpage'))
        else:
            return redirect(url_for('sessions.create_session', course_id=course_id))
    return render_template('portal/courses/sessions/create-session.html', students=students)
