from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, student_required
from portal.course import get_course

bp = Blueprint("student", __name__)


@bp.route("/student", methods=['GET'])
@student_required
@login_required
def student_view():
    sessions = []
    user_id = session.get('user_id')
    cur = db.get_db().cursor()
    cur.execute("""SELECT session_id from roster where student_id = %s""",
                (user_id,))
    student_classes = cur.fetchall()
    cur.close()

    for student_class in student_classes:
        cur = db.get_db().cursor()
        cur.execute("""SELECT sessions.id, sessions.course_id, sessions.location, sessions.days, sessions.class_time, courses.name AS class_name
                    FROM sessions JOIN courses on sessions.course_id = courses.course_id
                    WHERE sessions.id = %s""",
                    (student_class),)
        sessions = cur.fetchall()
        cur.close()

    return render_template("layouts/student-home.html", sessions=sessions)
