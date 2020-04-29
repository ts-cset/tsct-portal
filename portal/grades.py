from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request, flash
)
from portal.auth import teacher_required, login_required
from portal.db import get_db

bp = Blueprint('grades', __name__)

@bp.route('/grades', methods=("GET", "POST"))
@teacher_required
def grades():
    course_id = request.args.get('course_id')
    section = request.args.get('section')
    assign_id = request.args.get('assignment_id')

    assignents = assignments_info(assign_id)
    points_earned = request.form.getlist('grade')
    student = request.form.getlist('student')

    name = assignments[0][0]
    points = assignments[0][1]

    students = students_assigned(course_id, section)

    if request.method == "POST":
        grade_for(student[0], points_earned[0], assign_id)


    return render_template("portal/entergrades.html",
                            name=name,
                            points=points,
                            course_id=course_id,
                            students=students,
                            section=section)


def assignments_info(assign_id):
    cur = get_db().cursor()

    cur.execute("""SELECT name, points FROM assignments
                   WHERE id = %s;""",
                   (assign_id,))

    assignments = cur.fetchall()

    return assignments


def grade_for(student_sessions_id, points_earned, assignment_id):
    cur = get_db().cursor()
    cur.execute("""INSERT INTO grades (student_sessions_id, points_earned, assignment_id)
                   VALUES (%s, %s, %s)""",
                   (student_sessions_id, points_earned, assignment_id))
    get_db().commit()
    cur.close()


    #-- Gets all student id's that match course_id and section ---------------------
def student_sess_id(course_id, section):

    cur = get_db().cursor()
    cur.execute("""SELECT id
                   FROM student_sessions
                   WHERE course_id = %s AND section = %s;""",
                   (course_id, section))
    sessions = cur.fetchall()

    return sessions

def students_assigned(course_id, section):
    cur = get_db().cursor()
    cur.execute("""SELECT *
                   FROM users
                   JOIN student_sessions AS ss
                   ON users.id = ss.student_id
                   WHERE ss.course_id = %s AND ss.section = %s;""",
                   (course_id, section))
    student = cur.fetchall()
    return student
