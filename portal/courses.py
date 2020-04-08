from flask import (
    Blueprint, g, render_template, redirect, url_for, session
)

from portal.db import get_db

bp = Blueprint('courses', __name__)

@bp.route('/courses')
def courses():
    return render_template('portal/courses.html')

@bp.route('/courses/createcourse', methods=("POST",))
def courses_create():
    return redirect(url_for('courses.courses'))

@bp.route('/editcourse', methods=("GET", "POST"))
def courses_edit():
    return render_template('portal/editcourse.html')
