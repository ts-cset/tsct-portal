from flask import abort, Blueprint, g, render_template
from . import db
from portal.auth import login_required, teacher_required
from portal import sessions, assign, courses, submissions

bp = Blueprint("teacher_views", __name__)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/all_grades', methods=('GET', 'POST'))
@login_required
@teacher_required
def all_grades(course_id, sessions_id):
    """Teachers can view all of their students total
    grades with in a class session"""
    course = courses.get_course(course_id)
    session = sessions.get_session(sessions_id)
    students = get_students(sessions_id)
    # total_grade = submissions.letter_grade()
    with db.get_db() as con:
        with con.cursor() as cur:

                cur.execute(
                """SELECT assignments.id, assignments.sessions_id, assignments.points,
                submissions.id, submissions.grade, submissions.assignment_id,
                users.id, users.name, sessions.id, sessions.course_id
                FROM assignments INNER JOIN submissions ON assignments.id = submissions.assignment_id
                INNER JOIN users ON users.id = submissions.student_id
                INNER JOIN sessions ON sessions.id = assignments.sessions_id
                WHERE sessions.id = %s
                 """,
                 (sessions_id, )
                )
                student_grade = cur.fetchall()
                print(student_grade)




    return render_template("teacher_views/allGrades.html", course=course, session=session)


def get_students(sessions_id):

    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
            """SELECT sessions.course_id,
                      sessions.id,
                      courses.course_num,
                      users.name,
                      rosters.user_id,
                      rosters.session_id
                FROM users
                INNER JOIN rosters ON rosters.user_id = users.id
                INNER JOIN sessions ON sessions.id = rosters.session_id
                INNER JOIN courses ON courses.course_num = sessions.course_id
                WHERE session_id = %s """,
                (sessions_id, )
            )

            students = cur.fetchall()
            print(students)

            return students

# def get_total_grade(student, session)
#     with db.get_db() as con:
#         with con.cursor() as cur:
#
#             cur.execute(
#             """SELECT * FROM roster INNER JOIN users ON roster.user_id = user.id
#             INNER JOIN sessions on roster.session_id = sessions.id"""
#             )
