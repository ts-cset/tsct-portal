from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from portal.db import get_db

from portal.auth import login_required

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.route('/home')
@login_required
def home():
    # course_sessions is test data
    course_sessions = [{'session_name':'CSET'},
                       {'session_name':'brickZ'}]
    return render_template('student-page.html', course_sessions=course_sessions)
