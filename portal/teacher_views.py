from flask import abort, Blueprint, g, render_template
from . import db
from portal.auth import login_required, teacher_required
from portal import sessions, assign, courses, submissions

bp = Blueprint("teacher_views", __name__)

@bp.route('/course/<int:course_id>/session/<int:session_id>/all_grades', methods=('GET', 'POST'))
@login_required
@teacher_required
def all_grades():
    """Teachers can view all of their students total
    grades with in a class session"""
    course = courses.get_course(course_id)
    session = sessions.get_session(session_id)
    students = get_students(session_id)
    total_grade = submissions.letter_grade()
    with db.get_db() as con:
        with con.cursor() as cur:

            for student in students:
                pass



    return render_template("teacher_views/allGrades.html", course=course, session=session)


def get_students(session_id):

    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
            """SELECT sessions.session_name,
                      sessions.course_id,
                      sessions.id,
                      courses.course_num,
                      users.name,
                      users.email,
                      rosters.user_id,
                      rosters.session_id,

                FROM users
                INNER JOIN rosters ON rosters.user_id = users.id
                INNER JOIN sessions ON session.id = rosters.session_id
                INNER JOIN courses ON courses.course_num = session.course_id
                WHERE role = 'student' AND session_id = %s """
                (session_id, )
            )

# def get_total_grade(student, session)
#     with db.get_db() as con:
#         with con.cursor() as cur:
#
#             cur.execute(
#             """SELECT * FROM roster INNER JOIN users ON roster.user_id = user.id
#             INNER JOIN sessions on roster.session_id = sessions.id"""
#             )
