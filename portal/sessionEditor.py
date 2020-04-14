from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash
import functools
from . import courseEditor
from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("sessionEditor", __name__)

@bp.route("/courseSessions/<int:id>/edit/<int:session_id>", methods=('GET', 'POST'))
@login_required
@teacher_required
def session_edit(id, session_id):
    """Allows teachers to edit a specific session of a
    specific course"""
    course= get_course(id)

    return render_template("layouts/editSession.html")


@bp.route("/createSession/course/<int:id>", methods=('GET','POST'))
@login_required
@teacher_required
def session_create(id):
    """Allows a teacher to create a speficic session in  a
    specific course"""
    course = get_course(id)

    return render_template("layouts/createSession.html")


@bp.route("/courseSessions/<int:id>", methods=('GET', 'POST'))
@login_required
@teacher_required
def session_manage(id):
    """The management page of all the sessions in
    a specific course"""

    course = courseEditor.get_course(id)

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM sessions WHERE course_id = %s',
    (id, ))

    sessions = cur.fetchall()

    cur.close()

    return render_template("layouts/sessionManage.html", course=course, sessions=sessions)
