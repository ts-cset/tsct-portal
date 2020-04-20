from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role
from . import course

bp = Blueprint("session", __name__)

#Route for viewing sessions
@bp.route("/<int:id>/sessions", methods=['GET', 'POST'])
@login_required
def view_sessions(id):
    """Single page view of course"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM sessions where course = %s""",
                (id,))
    # cur.execute("""SELECT sessions.course, sessions.days, sessions.class_time, courses.teacherid, users.name AS teacher_name FROM sessions INNER JOIN users ON courses.teacherid = users.id WHERE courses.course_id = %s""",
    #             (id,))
    sessions = cur.fetchall()

    cur.execute("""SELECT courses.course_id, courses.name, courses.major, courses.description, courses.teacherid, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id WHERE courses.course_id = %s""",
                (id,))
    course = cur.fetchone()

    cur.close()

    return render_template("layouts/sessions/view_sessions.html", sessions=sessions, course=course)
