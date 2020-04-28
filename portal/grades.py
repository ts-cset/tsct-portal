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

    assignments = assignments_for_session(course_id, section)
    points_earned = 10

    for assignment in assignments:
        grade_for(assignment['student_sessions_id'], points_earned, assignment['id'])

    return render_template("portal/entergrades.html",
                                assignment=assignment,
                                course_id=course_id,
                                section=section)



def assignments_for_session(course_id, section):
    cur = get_db().cursor()

    cur.execute("""SELECT * FROM assignments AS a
                   JOIN sessions AS s
                   ON a.course_id = s.course_id
                   AND a.section = s.section
                   WHERE a.course_id = %s
                   AND a.section = %s;""",
                   (course_id, section))

    assignments = cur.fetchall()
    return assignments


def grade_for(student_sessions_id, points_earned, assignment_id):
    cur = get_db().cursor()
    cur.execute("""INSERT INTO grades (student_sessions_id, points_earned, assignment_id)
                   VALUES (%s, %s, %s)""",
                   (student_sessions_id, points_earned, assignment_id))
    get_db().commit()
    cur.close()
