from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin
from portal.teacher import bp

@bp.route('/assignments', methods=('GET', 'POST'))
@login_required
@admin
def assignments():
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                for item in request.form.getlist('id'):
                    cur.execute("""
                        DELETE FROM session_assignments
                        WHERE assignment_id = %s
                    """, (item,))
                    cur.execute("""
                        DELETE FROM assignments
                        WHERE id = %s
                    """, (item,))

    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT c.course_name, a.name, a.id
                FROM assignments a JOIN courses c
                ON a.course_id = c.id
                WHERE c.teacher_id = %s
            """, (g.user['id'],))
            assignments = cur.fetchall()

    return render_template('assignments.html', assignments=assignments)

@bp.route('/assignments/edit', methods=('GET', 'POST'))
@login_required
@admin
def edit_assignments():
    if request.method == 'POST':
        assignment_id = request.form['edit']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM assignments
                    WHERE id = %s
                    """, (assignment_id,))
                info = cur.fetchone()
        return render_template('edit-assignments.html', info=info)
    return redirect(url_for('teacher.assignments'))

@bp.route('/assignments/submit', methods=('GET', 'POST'))
@login_required
@admin
def submit_assignments():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        points = request.form['points']
        id = request.form['submit']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    UPDATE assignments
                    SET name = %s, description = %s, points = %s
                    WHERE id = %s
                """, (name, desc, points, id))
    return redirect(url_for('teacher.assignments'))
