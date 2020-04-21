from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, teacher_required
from portal.session import get_session

bp = Blueprint("roster", __name__)

# Route to roster
@bp.route("/<int:id>/roster", methods=('GET', 'POST'))
def view(id):
    # session_id = class_session['id']
    bname = ''
    con = db.get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT roster.student_id, roster.session_id, users.id, users.name
        FROM roster JOIN users ON roster.student_id = users.id
        WHERE session_id = %s ORDER BY users.name DESC""",
        (id,))
    students = cur.fetchall()
    cur.execute("""SELECT sessions.id, sessions.course_id, courses.course_id, courses.teacherid AS session_teacher
                FROM sessions JOIN courses on sessions.course_id = courses.course_id
                WHERE sessions.id = %s""",
                (id,))
    check = cur.fetchone()
    session_teacher = check['session_teacher']
    cur.close()
    if request.method == 'POST':
        message = ""
        studentname = request.form['sname']

        con = db.get_db()
        cur = con.cursor()
        cur.execute('SELECT id, name FROM users WHERE name = %s',
                    (studentname,))
        student = cur.fetchone()

        if student is not None:

            student_id = student['id']
            student_name = student['name']

            # cur.execute('SELECT count, student_id, session_id FROM roster WHERE student_id = %s AND session_id = %s',
            #             (student_id, id))
            # matching = cur.fetchone()
            # cur.close()

            con = db.get_db()
            cur = con.cursor()
            cur.execute(
                """INSERT INTO roster (student_id , session_id)
                    VALUES (%s, %s)""",
                (student_id, id))
            g.db.commit()
            cur.close()

        else:
            message = "Error: student not found"
        cur.close()
        con.close()
    return render_template("layouts/sessions/roster.html", students=students, session_teacher=session_teacher)
