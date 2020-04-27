from flask import abort, Blueprint, g, render_template
from . import db
from portal.auth import login_required, teacher_required
from portal import sessions, assign, courses

bp = Blueprint("teacher_views", __name__)

@bp.route('/course/<int:course_id>/session/<int:session_id>/all_grades', methods=('GET', 'POST'))
@login_required
@teacher_required
def all_grades():
    """Teachers can view all of their students total grades with in a class session"""
    return render_template("teacher_views/allGrades.html")
