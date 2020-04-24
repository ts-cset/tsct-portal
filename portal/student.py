from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, student_required
from portal.course import get_course

bp = Blueprint("student", __name__)


@bp.route("/student", methods=['GET'])
@student_required
@login_required
def student_view():
    sessions = []
    user_id = session.get('user_id')
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.course_id, sessions.location, sessions.days, sessions.class_time,
    courses.name AS class_name, roster.session_id
    FROM sessions JOIN courses on sessions.course_id = courses.course_id
    JOIN roster on roster.session_id = sessions.id
    JOIN users on users.id = roster.student_id
    WHERE users.id = %s""",
                (user_id,))
    student_classes = cur.fetchall()
    cur.close()

    return render_template("layouts/student-home.html", student_classes=student_classes)


@bp.route('/student/course/<int:course_id>/session/<int:session_id>/assignment/<int:id>/grade')
@login_required
@student_required
def assignment_grade(id, session_id, course_id):
    """student see grade for assignment"""

    user_id = session.get('user_id')

    cur = db.get_db().cursor()
    cur.execute("""SELECT (ROUND(grades.points_received/grades.total_points, 2 )*100) as assignment_grade,
                grades.total_points as total, grades.points_received as earned,
                grades.submission as submission, grades.feedback as feedback,
               grades.student_id, grades.assignment_id as assign_id, assignments.name as assign_name,
               assignments.description as description,
               grades.grade_id, roster.session_id as class_session, courses.name as name
	           FROM courses JOIN sessions on courses.course_id = sessions.id
	           JOIN assignments on assignments.session_id = sessions.id
               JOIN grades on grades.assignment_id = assignments.assignment_id
               JOIN roster on roster.session_id = sessions.id
               WHERE grades.assignment_id = %s
               AND grades.student_id = %s""",
                (id, user_id,))

    grade = cur.fetchone()
    cur.close()

    return render_template("/layouts/gradebook/assignment_grade.html", course_id=course_id, session_id=session_id,  id=id, grade=grade)


@bp.route("/student/gradebook", methods=['GET', 'POST'])
@student_required
@login_required
def view_student_gradebook():

    user_id = session.get('user_id')
    courses = []
    grades = []
    cur = db.get_db().cursor()
    cur.execute("""SELECT courses.course_id, courses.name AS class_name,
            users.name AS teacher, sessions.id AS session_id
            FROM roster JOIN sessions on roster.session_id = sessions.id
            JOIN courses on sessions.course_id = courses.course_id
            JOIN users on users.id = courses.teacherid
            WHERE roster.student_id =  %s """,
                (user_id,))
    courses = cur.fetchall()
    cur.close()

    return render_template("/layouts/gradebook/student_view.html", grades=grades, courses=courses)


@bp.route("/student/gradebook/course/<int:course_id>", methods=['GET', 'POST'])
@student_required
@login_required
def view_grades_by_course(course_id):

    user_id = session.get('user_id')

    cur = db.get_db().cursor()
    cur.execute("""SELECT (ROUND(sum(grades.points_received)/sum(grades.total_points), 2 )*100)
                 as total_grade,
                 (sum(grades.total_points)) as total, (sum(grades.points_received)) as earned,
                 grades.student_id, roster.session_id as class_session, courses.course_id,
                 courses.name as class_name
                 FROM courses JOIN sessions on courses.course_id = sessions.course_id
                 JOIN assignments on assignments.session_id = sessions.id
                 JOIN grades on grades.assignment_id = assignments.assignment_id
                 JOIN roster on roster.session_id = sessions.id
                 WHERE grades.student_id = %s AND courses.course_id = %s
	             GROUP BY grades.student_id, roster.session_id, courses.course_id""",
                (user_id, course_id))

    course_grade = cur.fetchone()

    cur.execute("""SELECT DISTINCT grades.grade_id,
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
    assignment_grades = cur.fetchall()
    cur.close()

    return render_template("/layouts/gradebook/course_grades.html", course_grade=course_grade, course_id=course_id, assignment_grades=assignment_grades)
