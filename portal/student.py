from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db

from portal.db import get_db

from portal.auth import login_required

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.route('/home')
@login_required
def home():
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT c.course_name, c.course_code, s.session_name, s.meeting_days,
                s.meeting_time, s.meeting_place, s.id, r.student_id
                FROM courses c JOIN sessions s
                ON c.id = s.course_id
                JOIN roster r
                ON s.id = r.session_id
                WHERE r.student_id = %s
                """, (g.user['id'],))
            courses = cur.fetchall()
    return render_template('student-page.html', courses=courses)

@bp.route('/assignments', methods=('GET', 'POST'))
@login_required
def assignments():
    if request.method == 'POST':
        session_id = request.form['session_id']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT a.name, a.description, a.points, s.due_date FROM assignments a JOIN session_assignments s
                    ON a.id = s.assignment_id
                    WHERE course_id IN (SELECT id FROM courses WHERE major = %s)
                    AND session_id = %s
                """, (g.user['major'], session_id,))
                assignments = cur.fetchall()
        return render_template('student-assignments.html', assignments=assignments)
    return redirect(url_for('student.home'))
