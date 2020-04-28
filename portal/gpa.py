from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("gpa", __name__)

@teacher_required
@login_required
@bp.route("/course/<int:course_id>/session/<int:id>/gpa", methods=('GET', 'POST'))
@teacher_required
@login_required
def view(id, course_id):
    course_name = course_id
    session_id = id
    return render_template("layouts/sessions/gpa.html", course_name=course_name, session_id=session_id)
