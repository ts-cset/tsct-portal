from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('portal', __name__, url_prefix='/portal')

@bp.route('/userpage')
@login_required
def userpage():
    return render_template('account/home.html')

@bp.route('/courses')
@login_required
def courses():
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses""")
    courses = cur.fetchall()
    cur.close()
    return render_template('portal/courses/index.html', courses=courses)

@bp.route('/view-session/<session_id>', methods=('GET', 'POST'))
@login_required
def view_session(session_id):
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
    return render_template('portal/courses/sessions/view-session.html', sessions=sessions, rosters=rosters)

@bp.route('/view-course/<course_id>', methods=('GET', 'POST'))
@login_required
def view_course(course_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur.execute("""SELECT * FROM session
                   WHERE courses_id = %s;""",
                   (course_id,))
    sessions = cur.fetchall()
    cur.close()
    return render_template('portal/courses/view-course.html', courses=courses, sessions=sessions)

@bp.route('/create-course', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_course():
    if request.method == 'POST':
        course_number = request.form['course_number']
        name = request.form['name']
        description = request.form['description']
        credits = request.form['credits']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
         INSERT INTO courses (course_number, major, name, description, credits, teacher)
         VALUES (%s, %s, %s, %s, %s, %s);
         """,
         (course_number, g.users['major'], name, description, credits, g.users['id']))
        db.get_db().commit()
        cur.close()

        if error is None:
            return redirect(url_for('portal.userpage'))
    return render_template('portal/courses/create-course.html')

@bp.route('/update-course/<course_id>', methods=('GET', 'POST'))
@login_required
@teacher_required
def update_course(course_id):
    if request.method == 'POST':
        course_number = request.form['course_number']
        name = request.form['name']
        description = request.form['description']
        credits = request.form['credits']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
         UPDATE courses SET course_number = %s, major = %s, name = %s, description = %s, credits = %s, teacher = %s
         WHERE id = %s;
         """,
         (course_number, g.users['major'], name, description, credits, g.users['id'], id))
        db.get_db().commit()
        cur.close()

        if error is None:
            return redirect(url_for('portal.userpage'))
    return render_template('portal/courses/update-course.html')

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
        print(students)
        error = None
        cur = db.get_db().cursor()
        cur.execute("""INSERT INTO session (courses_id, times, name)
        VALUES (%s, %s, %s);
         """,
         (course_id, times, name))
        db.get_db().commit()
        cur.execute("""SELECT id FROM session
                       WHERE courses_id = %s""",
                       (course_id,))
        session = cur.fetchone()
        print(session)

        for student in students:
            cur.execute("""INSERT INTO roster (users_id, session_id)
            VALUES (%s, %s);
             """,
             (student, session[0]))
            db.get_db().commit()
        cur.close()

        if error is None:
            return redirect(url_for('portal.userpage'))
    return render_template('portal/courses/sessions/create-session.html', students=students)
