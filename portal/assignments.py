from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request
)

from portal.db import get_db

bp = Blueprint('assignments', __name__)

@bp.route('/assignments')
def assignments():
    """View for the assignments"""
    if session['user'][4] == 'student':
    # get the id of the student
        student = session['user'][0]
    # Display the student's assignments
        cur = get_db().cursor()

    # pulls out all assignments for student id
        cur.execute("SELECT * FROM assignments JOIN student_sessions ON student_sessions_id = student_sessions.id WHERE student_id = %s;", (student,))
        student_assignments = cur.fetchall()

    else:
        return render_template('portal/home.html')

    return render_template("portal/assignments.html", student_assignments=student_assignments)
