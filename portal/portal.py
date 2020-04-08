from flask import redirect, g, url_for, render_template, session, request, Blueprint

from . import db

bp = Blueprint("portal", __name__)


@bp.route("/courseManagement", methods=('GET', 'POST'))
def course_manage():
    """Allows teachers to have a page which allows
    them to edit and create courses"""
    return render_template("layouts/courseMan.html")


@bp.route("/courseCreate", methods=('GET', 'POST'))
def course_create():
    """Allows the teacher to create a course and fill out specifics on course"""
    pass


@bp.route("/courseInfo<ID>")
def course_info():
    """Allows teachers to see current info on a course they own"""
    pass
