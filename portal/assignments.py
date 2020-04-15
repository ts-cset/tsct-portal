from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request
)

from portal.db import get_db

bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=('GET'))
def assignments():
    """View for the assignments"""
    if session ['user'][3] == 'student':
    # get the id of the student
        student = session['user'][1]
    # Display the student's assignments
        cur = get_db().cursor()

        cur.execute("SELECT * FROM assignments JOIN student_sessions ON student_sessions_id = student_sessions.id WHERE student_id = ?;")
        student_assignments = cur.fetchall()
    else:
        return render_template('portal/home.html')

    return render_template("portal/assignments.html", student_assignments=student_assignments)
