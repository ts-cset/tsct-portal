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

@bp.route('<assignment_id>/submit-assignment', methods=('GET', 'POST'))
@login_required
def submit_assignment(assignment_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE id = %s;""",
                   (assignment_id,))
    assignments = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        answer = request.form['answer']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        UPDATE submissions SET answer = %s
        WHERE users_id = %s and assignments_id = %s;""",
        (answer, g.users['id'], assignment_id))
        db.get_db().commit()

        if error is None:
            return redirect(url_for('portal.userpage'))
    return render_template('portal/courses/sessions/assignments/submit-assignments.html', assignments=assignments)

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
            cur.execute("""
            SELECT id FROM assignments
            WHERE name = %s and session_id = %s;
            """,
            (name, session_id))
            assignments = cur.fetchone()
            assignment_id = assignments[0]
            cur.execute("""
            SELECT users.id FROM users
            JOIN roster ON roster.users_id = users.id
            JOIN session ON session.id = roster.session_id
            WHERE session_id = %s;
            """,
            (session_id,))
            students = cur.fetchall()
            for student in students:
                cur.execute("""INSERT INTO submissions (users_id, assignments_id)
                VALUES (%s, %s);
                 """,
                 (student[0], assignment_id))
                db.get_db().commit()
            cur.close()


            return redirect(url_for('portal.userpage'))
        else:
            return redirect(url_for('assignments.create_assignment', session_id=session_id))
    return render_template('portal/courses/sessions/assignments/create-assignments.html')
