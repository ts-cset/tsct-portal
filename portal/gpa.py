from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("gpa", __name__)

@teacher_required
@login_required
@bp.route("/course/<int:course_id>/session/<int:id>/gpa", methods=('GET', 'POST'))
@teacher_required
@login_required
def view(id, course_id):
    course_name = course_id
    session_id = id
    grades = get_grades(id , course_id)
    return render_template("layouts/sessions/gpa.html", grades= grades, course_name=course_name, session_id=session_id)

def get_grades(session, course):
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
        """SELECT (ROUND(sum(grades.points_received)/sum(grades.total_points), 2 )*100)
                 as total_grade, (sum(grades.total_points)) as total, (sum(grades.points_received)) as earned, grades.student_id, roster.session_id as class_session, courses.course_id,
                 courses.name as class_name
                 FROM courses JOIN sessions on courses.course_id = sessions.course_id
                 JOIN assignments on assignments.session_id = sessions.id
                 JOIN grades on grades.assignment_id = assignments.assignment_id
                 JOIN roster on roster.session_id = sessions.id
                 WHERE courses.course_id = %s AND sessions.id = %s
	             GROUP BY grades.student_id, roster.session_id, courses.course_id""",
                 (course , session))
        grades = cur.fetchall()
        cur.close()
        con.close()
        return grades
