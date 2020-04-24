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
        return render_template('assignments/edit-assignments.html', info=info)
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
@bp.route('/assignments/grade', methods=('GET','POST'))
@login_required
@admin
def grade():
    if request.method == 'POST':
        code = request.form['grade']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT r.name, r.description, r.points, u.first_name, u.last_name, u.id, a.work_id
                FROM session_assignments a JOIN assignments r
                ON a.assignment_id = r.id
                JOIN roster d
                ON a.session_id = d.session_id
                JOIN users u
                ON d.student_id = u.id
                WHERE a.assignment_id = %s
                """, (code, ))
                students = cur.fetchall()
                print(students)
        return render_template('assignments/teacher-assignments.html', students=students)
    return redirect(url_for('teacher.courses'))
@bp.route('/assignments/view', methods=('GET', 'POST'))
@login_required
@admin
def view_assignments():
    if request.method == 'POST':
        code = request.form['view-grade']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT a.name, a.description, a.points, c.course_name, a.id, p.work_id
                FROM sessions s JOIN session_assignments p
                ON s.id = p.session_id
                JOIN assignments a
                ON p.assignment_id = a.id
                JOIN courses c
                ON c.id = s.course_id
                WHERE s.id = %s
                """, (code,))
                assignments = cur.fetchall()
            print(code)
            print(assignments)
        return render_template('assignments/view-assignments.html', assignments=assignments)

    return redirect(url_for('teacher.courses'))
@bp.route('/grade/submission', methods=('GET', 'POST'))
@login_required
@admin
def grade_submission():
    if request.method == 'POST':
        grade = request.form['grade-submission']
        user = list(request.form['submission'])
        with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                    SELECT * FROM assignment_grades
                    WHERE owner_id = %s AND assigned_id = %s
                    """, (user[1], user[4], ))
                    search = cur.fetchall()
                    print(search)
                    print(type(search))
        if not search:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                    INSERT INTO assignment_grades(owner_id, assigned_id, grades) VALUES (%s, %s, %s);
                    SELECT * FROM assignment_grades
                    """, (user[1], user[4], grade, ))
                    res = cur.fetchall()
                    print(res)
                    print('Has been registered')
                    return redirect(url_for('teacher.sessions'))
        else :
              with db.get_db() as con:
                  with con.cursor() as cur:
                      cur.execute("""
                      UPDATE assignment_grades
                      SET grades = %s
                      WHERE owner_id = %s AND assigned_id = %s;
                      SELECT * FROM assignment_grades
                      """, (grade ,user[1], user[4],))
                      res = cur.fetchall()
                      print(res)
                      return redirect(url_for('teacher.sessions'))
    return redirect(url_for('teacher.courses'))
