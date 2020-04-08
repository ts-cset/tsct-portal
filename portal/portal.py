from flask import redirect, g, url_for, render_template, session, request, Blueprint

from . import db

bp = Blueprint("portal", __name__)


@bp.route("/courseManagement", methods=('GET', 'POST'))
def course_manage():
    """Allows teachers to have a page which allows
    them to edit and create courses"""
    if request.method == 'POST':
        with get_db() as con:
            with con.cursor() as cur:
                pass

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM courses')
    course = cur.fetchall()
    cur.close()
    return render_template("layouts/courseMan.html", course=course)


@bp.route("/courseCreate", methods=('GET', 'POST'))
def course_create():
    """Allows the teacher to create a course and fill out specifics on course"""
    if request.method == 'POST':
        with get_db() as con:
            with con.cursor() as cur:
                pass

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM courses')
    course = cur.fetchall()
    cur.close()
    return render_template("layouts/courseMan.html", course=course)


@bp.route("/courseEdit", methods=('GET', 'POST'))  # Needs new template
def course_edit():
    """Allows user to edit the course"""
    pass


@bp.route("/courseInfo", methods=('GET', 'POST'))  # Needs new template
def course_info():
    """Allows teachers to see current info on a course they own"""
    pass
