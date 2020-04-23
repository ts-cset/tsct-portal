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
    cur.execute("""SELECT session_id from roster where student_id = %s""",
                (user_id,))
    student_classes = cur.fetchall()
    cur.close()

    for student_class in student_classes:
        cur = db.get_db().cursor()
        cur.execute("""SELECT sessions.id, sessions.course_id, sessions.location, sessions.days, sessions.class_time, courses.name AS class_name
                    FROM sessions JOIN courses on sessions.course_id = courses.course_id
                    WHERE sessions.id = %s""",
                    (student_class),)
        sessions = cur.fetchall()
        cur.close()

    return render_template("layouts/student-home.html", sessions=sessions)


@bp.route('/student/course/<int:course_id>/session/<int:session_id>/assignment/<int:id>/grade')
@login_required
@student_required
def view_assignment_grade(id, session_id, course_id):
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

    return render_template("/layouts/assignments/view_assignment_grade.html", course_id=course_id, session_id=session_id,  id=id, grade=grade)
