from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role
from . import course

bp = Blueprint("assignment", __name__)


@bp.route('/<int:id>/create_assignment', methods=('GET', 'POST'))
@login_required
def create_assignment(id):
    """Single page view to create an assignment."""

    if request.method == 'POST':

        session_id = id
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['date']

        con = db.get_db()
        cur = con.cursor()
        cur.execute("""
        INSERT INTO assignments(session_id, name, description, due_date)
        VALUES (%s, %s, %s, %s)""",
        (session_id, name, description, due_date));
        g.db.commit()
        cur.close()
        con.close()
        return redirect(url_for('assignment.view_assignments', id=id))

    return render_template('layouts/assignments/create_assignments.html')


@bp.route('/<int:id>/assignments', methods=('GET',))
@login_required
def view_assignments(id):
    """Single page view of all the assignments in a session."""

    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
    SELECT * FROM assignments
    WHERE session_id = %s
    """, (id,))

    assignments = cur.fetchall()
    cur.close()
    con.close()


    return render_template('layouts/assignments/view_assignments.html', id=id, assignments=assignments)

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_assignments(id):
    """Singe page view to edit an assignment."""

    con = db.get_db()
    cur = con.cursor()
    if request.method == 'POST':

        session_id = id
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['date']

        cur.execute("""
        UPDATE assignments SET name = %s, decription = %s, due_date= %s
        WHERE assignment_id = %s
        """, (name, description, due_date, session_id))
        g.db.commit()

    cur.close()
    con.close()
