from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("session", __name__)


def get_session(id):

    user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.id, sessions.course_id, sessions.class_time,
                sessions.days, courses.teacherid AS course_teacher, courses.course_id
                FROM sessions JOIN courses on sessions.course_id = courses.course_id
                WHERE courses.teacherid = %s AND sessions.id = %s""",
                (user_id, id,))
    class_session = cur.fetchone()
    cur.close()

    if session is None:
        abort(400, """System has prevented this action. \n
              Either this session does not exist,\n
              or you do not have acces to it.""")

    return class_session

# Route for viewing sessions
@bp.route("/<int:id>/sessions", methods=['GET', 'POST'])
@login_required
def view_sessions(id):
    """Single page view of session"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.id, sessions.days, sessions.course_id,
                sessions.class_time, courses.name AS course_name,
                courses.teacherid AS teacher_id
                FROM sessions JOIN courses ON courses.course_id = sessions.course_id
                WHERE sessions.course_id = %s""",
                (id,))
    sessions = cur.fetchall()
    cur.close()

    return render_template("layouts/sessions/view_sessions.html", sessions=sessions)


@login_required
@teacher_required
@bp.route("/sessions/<int:id>/edit", methods=['GET', 'POST'])
def session_edit(id):
    """Edit a session"""
    session = get_session(id)
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
        g.db.close()

        return redirect(url_for('session.view_sessions', id=session['course_id']))

    return render_template("layouts/sessions/edit_session.html", session=session)


@bp.route("/sessions/create", methods=['GET', 'POST'])
@teacher_required
@login_required
def create():

    teacherid = session['user_id']
    cur = db.get_db().cursor()
    cur.execute("""
        SELECT course_id, name FROM courses where teacherid=%s""",
                (teacherid,))
    courses = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        course = request.form['courses']
        cur = db.get_db().cursor()
        cur.execute("""
            SELECT course_id FROM courses where name=%s""",
                    (course,))
        x = cur.fetchone()
        cur.close()
        course_id = x['course_id']
        days = request.form['session_days']
        class_time = request.form['class_time']
        print(course, course_id, days, class_time)
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO sessions ( course_id, days, class_time)
        VALUES ( %s, %s, %s)""",
                    (course_id, days, class_time))

        g.db.commit()
        cur.close()
        return redirect(url_for('session.view_sessions', id=course_id))

    return render_template("layouts/sessions/create_session.html", courses=courses)


@bp.route("/session/<int:id>/delete", methods=['POST', 'GET'])
@teacher_required
@login_required
def delete_session(id):
    """Delete unwanted session"""
    x = get_session(id)
    course_id = x['course_id']
    cur = db.get_db().cursor()
    cur.execute('DELETE FROM sessions where id = %s',
                (id,))
    g.db.commit()
    cur.close()
    return redirect(url_for('session.view_sessions', id=course_id))
