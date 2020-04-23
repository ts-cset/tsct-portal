from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, teacher_required
from . import course

bp = Blueprint("assignment", __name__)


def get_assignment(id):

    user_id = session.get('user_id')

    con = db.get_db()
    cur = con.cursor()
    cur.execute("""SELECT assignments.assignment_id, assignments.session_id,
                sessions.course_id, courses.teacherid
                FROM assignments JOIN sessions ON assignments.session_id = sessions.id
                JOIN courses ON sessions.course_id = courses.course_id
                WHERE assignments.assignment_id = %s
                AND courses.teacherid = %s""",
                (id, user_id))
    check_teacher = cur.fetchone()
    cur.close()

    if check_teacher is None:
        con.close()
        abort(400, """You cannot modify this assignment""")
    else:
        cur = con.cursor()
        cur.execute("""SELECT assignments.assignment_id, assignments.name, assignments.description,
                    assignments.due_date
                    FROM assignments
                    WHERE assignment_id = %s""",
                    (id,))
        assignment = cur.fetchone()
        cur.close()

        return assignment


@bp.route('/course/<int:course_id>/session/<int:id>/create_assignment', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_assignment(id, course_id):
    """Single page view to create an assignment."""
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""SELECT sessions.course_id, courses.course_id, courses.name
                AS class_name FROM sessions JOIN courses
                ON sessions.course_id=sessions.course_id
                WHERE sessions.id=%s""",
                (id,))
    course = cur.fetchone()
    cur.close()

    if request.method == 'POST':

        # Getting all information necessary for creating an assignment
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['date']

        con = db.get_db()
        cur = con.cursor()

        # Query to actually insert assignment into the database
        cur.execute("""
        INSERT INTO assignments(session_id, name, description, due_date)
        VALUES (%s, %s, %s, %s)""",
                    (id, name, description, due_date))
        g.db.commit()

        cur.close()
        con.close()
        return redirect(url_for('assignment.view_assignments', id=id, course_id=course_id))

    con.close()

    return render_template('layouts/assignments/create_assignments.html', course=course)


@bp.route('/course/<int:course_id>/session/<int:id>/assignments', methods=('GET',))
@login_required
def view_assignments(id, course_id):
    """Single page view of all the assignments in a session."""

    con = db.get_db()
    cur = con.cursor()

    cur.execute("""SELECT sessions.id, sessions.course_id, courses.course_id,
                courses.teacherid, courses.name
                AS class_name FROM sessions JOIN courses
                ON sessions.course_id = sessions.course_id
                WHERE sessions.id=%s AND courses.course_id= %s""",
                (id, course_id,))
    course = cur.fetchone()

    # Query to get all of the asssignments in a session
    cur.execute("""
    SELECT * FROM assignments
    WHERE session_id = %s
    ORDER BY assignment_id ASC
    """, (id,))

    assignments = cur.fetchall()
    cur.close()
    con.close()

    return render_template('layouts/assignments/view_assignments.html', course=course, id=id, assignments=assignments)


@bp.route('/course/<int:course_id>/session/<int:session_id>/assignment/<int:id>/edit-assignment', methods=('GET', 'POST'))
@login_required
@teacher_required
def edit_assignments(course_id, session_id, id):
    """Singe page view to edit an assignment."""

    assignment = get_assignment(id)

    if request.method == 'POST':

        # getting all info required to update assignment information
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['date']

        con = db.get_db()
        cur = con.cursor()
        # Query to update the information for an assignment
        cur.execute("""
        UPDATE assignments SET name = %s, description = %s, due_date= %s
        WHERE assignment_id = %s
        """, (name, description, due_date, id))

        # Query to return directly to whichever session the assignment was from
        cur.execute("""
        SELECT * FROM assignments
        WHERE assignment_id = %s""", (id,))
        session_id = cur.fetchone()
        g.db.commit()
        cur.close()
        con.close()

        return redirect(url_for('assignment.view_assignments', id=session_id['session_id'], course_id=course_id))

    return render_template('layouts/assignments/edit_assignments.html', assignment=assignment)


@bp.route('/course/<int:course_id>/session/<int:session_id>/assignment/<int:id>/delete', methods=['POST'])
@login_required

def delete_assignments(id, course_id, session_id):

    """Deletes any unwanted assignments."""

    con = db.get_db()
    cur = con.cursor()

    # Query to delete an assignment from the database
    cur.execute("""
    DELETE FROM assignments WHERE assignment_id = %s
    """, (id,))
    g.db.commit()

    cur.close()
    con.close()

    return redirect(url_for('assignment.view_assignments', id=session_id, course_id=course_id))
