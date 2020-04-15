from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('assignments', __name__, url_prefix='/portal/assignments')

@bp.route('/<course_id>/<session_id>/view-assignment/<assignment_id>', methods=('GET', 'POST'))
@login_required
def view_assignment(course_id, session_id, assignment_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM session
                   WHERE id = %s;""",
                   (session_id,))
    sessions = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE id = %s;""",
                   (assignment_id,))
    assignments = cur.fetchall()
    cur.close()
    return render_template('portal/courses/sessions/assignments/view-assignment.html', courses=courses, sessions=sessions, assignments=assignments)

@bp.route('/<session_id>/create-assignment', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_assignment(session_id):

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        points = request.form['points']
        description = request.form['description']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM assignments
        WHERE name = %s and session_id = %s;
        """,
        (name, session_id))
        assignment = cur.fetchone()

        if assignment != None:
            error = "That assignment already exists"

        if error is None:
            cur.execute("""INSERT INTO assignments (session_id, name, date, description, points)
            VALUES (%s, %s, %s, %s, %s);
             """,
             (session_id, name, date, description, points))
            db.get_db().commit()
            cur.close()


            return redirect(url_for('portal.userpage'))
        else:
            return redirect(url_for('assignments.create_assignment', session_id=session_id))
    return render_template('portal/courses/sessions/assignments/create-assignments.html')
