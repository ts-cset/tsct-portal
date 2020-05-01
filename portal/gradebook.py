from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('gradebook', __name__, url_prefix='/portal/gradebook')

@bp.route('/')
@login_required
def gradebook():
    if g.users['role'] == 'teacher':
        cur = db.get_db().cursor()
        cur.execute("""SELECT * FROM courses""")
        courses = cur.fetchall()
        cur.execute("""SELECT courses.id AS c_id, session.* FROM session
                       JOIN courses ON courses.id = session.courses_id""")
        sessions = cur.fetchall()
        cur.execute("""SELECT session.id AS s_id, users.id AS u_id, SUM(submissions.points) AS s_points, SUM(assignments.points) AS a_points, '' as grade FROM users
                    JOIN roster ON roster.users_id = users.id
                    JOIN session ON roster.session_id = session.id
                    JOIN assignments ON assignments.session_id=session.id
                    JOIN submissions ON submissions.assignments_id = assignments.id and users.id = submissions.users_id
                    GROUP BY session.id, users.id
                    ORDER BY session.id""")
        grades = cur.fetchall()
    else:
        cur = db.get_db().cursor()
        cur.execute("""
            SELECT DISTINCT ON (courses.id) roster.*, users.*, session.*, courses.* FROM roster
            JOIN users ON users.id = roster.users_id
            JOIN session ON session.id = roster.session_id
            JOIN courses ON courses.id = session.courses_id
            WHERE users.id = %s;""",
            (g.users['id'],))
        courses = cur.fetchall()
        cur.execute("""
            SELECT DISTINCT ON (session.id) session.*, roster.id AS r_id, users.id AS u_id, courses.id AS c_id FROM roster
            JOIN users ON users.id = roster.users_id
            JOIN session ON session.id = roster.session_id
            JOIN courses ON courses.id = session.courses_id
            WHERE users.id = %s;""",
            (g.users['id'],))
        sessions = cur.fetchall()
        cur.execute("""SELECT session.id AS s_id, users.id AS u_id, SUM(submissions.points) AS s_points, SUM(assignments.points) AS a_points, '' as grade FROM users
                    JOIN roster ON roster.users_id = users.id
                    JOIN session ON roster.session_id = session.id
                    JOIN assignments ON assignments.session_id=session.id
                    JOIN submissions ON submissions.assignments_id = assignments.id and users.id = submissions.users_id
                    WHERE users.id = %s
                    GROUP BY session.id, users.id
                    ORDER BY session.id""",
                    (g.users['id'],))
        grades = cur.fetchall()

    for grade in grades:
        grade[4] = grade[2]/grade[3]

        if grade[4] >= 0.98:
            grade[4] = 'A+'
        elif grade[4] >= 0.93:
            grade[4] = 'A'
        elif grade[4] >= 0.90:
            grade[4] = 'A-'
        elif grade[4] >= 0.87:
            grade[4] = 'B+'
        elif grade[4] >= 0.83:
            grade[4] = 'B'
        elif grade[4] >= 0.80:
            grade[4] = 'B-'
        elif grade[4] >= 0.77:
            grade[4] = 'C+'
        elif grade[4] >= 0.73:
            grade[4] = 'C'
        elif grade[4] >= 0.70:
            grade[4] = 'C-'
        elif grade[4] >= 0.67:
            grade[4] = 'D+'
        elif grade[4] >= 0.63:
            grade[4]= 'D'
        elif grade[4] >= 0.60:
            grade[4] = 'D-'
        else:
            grade[4] = 'F'

    cur.close()
    return render_template('portal/gradebook/view-gradebook.html', courses=courses, sessions=sessions, grades=grades)
