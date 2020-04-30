from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, student_required
from portal.course import get_course

bp = Blueprint("student", __name__)


@bp.route("/student", methods=['GET'])
@login_required
@student_required
def student_view():
    sessions = []
    user_id = session.get('user_id')
    con = db.get_db()
    cur = con.cursor()
    cur.execute("""SELECT sessions.course_id, sessions.location, sessions.days, sessions.class_time,
    courses.name AS class_name, roster.session_id
    FROM sessions JOIN courses on sessions.course_id = courses.course_id
    JOIN roster on roster.session_id = sessions.id
    JOIN users on users.id = roster.student_id
    WHERE users.id = %s""",
                (user_id,))
    student_classes = cur.fetchall()

    cur.execute("""SELECT major FROM users
                WHERE id = %s""",
                (user_id,))
    student_major = cur.fetchone()
    cur.close()
    con.close()

    return render_template("layouts/student-home.html", student_classes=student_classes, student_major=student_major)


@bp.route('/student/course/<int:course_id>/session/<int:session_id>/assignment/<int:id>/grade')
@login_required
@student_required
def assignment_grade(id, session_id, course_id):
    """student see grade for assignment"""

    user_id = session.get('user_id')


<< << << < HEAD
    con = db.get_db()
    cur = con.cursor()
    cur.execute("""SELECT (ROUND(grades.points_received/grades.total_points, 2 )*100) as assignment_grade,
=======
    cur = db.get_db().cursor()
    cur.execute("""SELECT DISTINCT(ROUND(grades.points_received / grades.total_points, 2) * 100) as assignment_grade,
>>>>>> > 38fcd03cf03fb074bfe4016a0695b48dc5075de0
                grades.total_points as total, grades.points_received as earned,
                grades.submission as submission, grades.feedback as feedback,
               grades.student_id, grades.assignment_id as assign_id, assignments.name as assign_name,
               assignments.description as description,
               grades.grade_id, roster.session_id as class_session, courses.name as name
	           FROM courses JOIN sessions on courses.course_id=sessions.id
	           JOIN assignments on assignments.session_id=sessions.id
               JOIN grades on grades.assignment_id=assignments.assignment_id
               JOIN roster on roster.session_id=sessions.id
               WHERE grades.assignment_id=% s
               AND grades.student_id=% s""",
                (id, user_id,))

    grade = cur.fetchone()
    cur.close()
    con.close()

    return render_template("/layouts/gradebook/assignment_grade.html", course_id=course_id, session_id=session_id,  id=id, grade=grade)


@bp.route("/student/gradebook", methods=['GET', 'POST'])
@login_required
@student_required
def view_student_gradebook():

    user_id = session.get('user_id')
    courses = []
    grades = []
<<<<<<< HEAD
    con = db.get_db()
    cur = con.cursor()
    cur.execute("""SELECT courses.course_id, courses.name AS class_name,
== == == =
    cur=db.get_db().cursor()
    cur.execute("""SELECT DISTINCT courses.course_id, courses.name AS class_name,
>>>>>>> 38fcd03cf03fb074bfe4016a0695b48dc5075de0
            users.name AS teacher, sessions.id AS session_id
            FROM roster JOIN sessions on roster.session_id = sessions.id
            JOIN courses on sessions.course_id = courses.course_id
            JOIN users on users.id = courses.teacherid
            WHERE roster.student_id =  %s """,
                (user_id,))
    courses=cur.fetchall()
    cur.close()
    con.close()

    return render_template("/layouts/gradebook/student_view.html", grades=grades, courses=courses)


@bp.route("/student/gradebook/course/<int:course_id>/session/<int:session_id>", methods=['GET', 'POST'])
@student_required
@login_required
def view_grades_by_course(course_id, session_id):

    user_id=session.get('user_id')

    cur=db.get_db().cursor()

    # Get all of the grades in the course for a student
    cur.execute("""
    SELECT * FROM grades
    JOIN assignments ON assignments.assignment_id = grades.assignment_id
    WHERE student_id = %s AND points_received IS NOT NULL
    AND session_id = %s
    """, (user_id, session_id))

    course_grade=cur.fetchall()

    points_received=0
    total_points=0

    # calculate the points for the grade
    for grade in course_grade:

        total_points=total_points + grade['total_points']
        points_received=points_received + grade['points_received']

    # if there's no assignments, students still have %100 grade
    if total_points == 0:
        current_grade=100
    else:
        current_grade=(points_received / total_points) * 100

    cur.execute("""SELECT DISTINCT grades.grade_id, sessions.id,
            (ROUND(grades.points_received/grades.total_points, 2 )*100) as assignment_grade,
            grades.total_points as total, grades.points_received as earned,
            grades.assignment_id as assign_id, assignments.name as assign_name
            FROM courses JOIN sessions on courses.course_id = sessions.course_id
            JOIN assignments on assignments.session_id = sessions.id
            JOIN grades on grades.assignment_id = assignments.assignment_id
            JOIN roster on roster.session_id = sessions.id
            WHERE grades.student_id = %s
            AND courses.course_id = %s""",
                (user_id, course_id))
    assignment_grades=cur.fetchall()

    cur.close()
    con.close()

    return render_template("/layouts/gradebook/course_grades.html", course_id=course_id,
    assignment_grades=assignment_grades, points_received=points_received, total_points=total_points,
    current_grade=current_grade, course_grade=course_grade)
