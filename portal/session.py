from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role

bp = Blueprint("session", __name__)

# Route for viewing sessions
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
