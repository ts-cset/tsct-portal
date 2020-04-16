from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role

bp = Blueprint("portal", __name__)


@bp.route('/')
def index():
    return render_template('layouts/index.html')


@bp.route("/home", methods=['GET', 'POST'])
@login_role
@login_required
def home():

    user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute(
        """SELECT courses.course_id, courses.name, courses.major, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id""")
    courses = cur.fetchall()
    cur.close()
    print(courses)

    return render_template("layouts/home.html", courses=courses)


def get_course(id, check_teacher=True):

    user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute("""SELECT course_id, name, description, teacherid FROM courses WHERE teacherid = %s AND course_id = %s""",
                (user_id, id,))
    course = cur.fetchone()
    cur.close()

    if course is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_teacher and course['teacherid'] != g.user['id']:
        abort(403)

    return course


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
@login_role
@login_required
def view(id):
    """Single page view of course"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT courses.course_id, courses.name, courses.major, courses.description, courses.teacherid, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id WHERE courses.course_id = %s""",
                (id,))
    course = cur.fetchone()
    cur.close()

    return render_template("layouts/courses/view_course.html", course=course)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_role
@login_required
def edit(id):
    """Edits the description of the courses"""
    course = get_course(id)

    if request.method == 'POST':

        teacherid = session['user_id']
        course_name = request.form['new_course']
        course_description = request.form['course_description']

        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE courses SET name = %s, description = %s'
            ' WHERE course_id = %s ',
            (course_name, course_description, id)
        )
        g.db.commit()
        cur.close()

        return redirect(url_for('portal.home'))

    return render_template("layouts/courses/edit.html", course=course)


@bp.route("/<int:id>/delete", methods=["POST", ])
@login_role
@login_required
def delete(id):
    """delete unwanted tasks"""
    course = get_course(id)
    cur = db.get_db().cursor()
    cur.execute(
        'DELETE FROM courses WHERE course_id= %s', (id,)
    )
    g.db.commit()
    cur.close()
    return redirect(url_for('portal.home'))


@bp.route("/student")
@login_required
def student():
    return render_template("layouts/student-home.html")


@bp.route("/create", methods=['GET', 'POST'])
@login_role
@login_required
def create():

    cur = db.get_db().cursor()
    cur.execute("""
        SELECT major_id, name FROM majors""",
                )
    majors = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        teacherId = session['user_id']
        major = request.form['majors']
        course_name = request.form['new_course']
        course_description = request.form['course_description']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO courses (name, major, description, teacherId)
        VALUES (%s, %s, %s, %s)""",
                    (course_name, major, course_description, teacherId,))

        g.db.commit()
        return redirect(url_for('portal.home'))

    return render_template("layouts/courses/create_courses.html", majors=majors)


@bp.route("/<int:id>/sessions", methods=['GET', 'POST'])
@login_required
def view_sessions(id):
    """Single page view of session"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.id, sessions.course, sessions.days, sessions.class_time, courses.teacherid AS teacher_id FROM sessions FULL JOIN courses ON courses.course_id = sessions.course WHERE sessions.course = %s""",
                (id,))
    sessions = cur.fetchall()
    cur.close()

    return render_template("layouts/sessions/view_sessions.html", sessions=sessions)


@bp.route("/sessions/create", methods=['GET', 'POST'])
@login_role
@login_required
def create(id):

    if request.method == 'POST':

        teacherid = session['user_id']
        session_days = request.form['session_days']
        session_time = request.form['session_time']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO sessions (course, teacher, days, class_time)
        VALUES (%s, %s, %s, %s)""",
                    (id, teacherid, session_days, session_time,))

        g.db.commit()
        return redirect(url_for('portal.view', id=id))

    return render_template("layouts/sessions/create_sessions.html")


@bp.route("/<int:id>/sessions/edit", methods=['GET', 'POST'])
@login_required
@login_role
def edit_session(id):
    """Edit a session"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM sessions WHERE id = %s""",
                (id,))
    session = cur.fetchone()
    cur.close()

    if request.method == 'POST':

        session_days = request.form['session_days']
        session_time = request.form['session_time']

        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE sessions SET days = %s, class_time = %s'
            ' WHERE id = %s ',
            (session_days, session_time, id)
        )
        g.db.commit()
        cur.close()

        return redirect(url_for('portal.view_sessions', id=session['course']))

    return render_template("layouts/sessions/edit_session.html", session=session)
