from flask import (
    render_template, Blueprint, session, g, flash, request, redirect, url_for, abort
)

from . import db, auth

bp = Blueprint("submissions", __name__)

@bp.route('/course/<int:course_id>/session/<int:session_id>/assignments/<int:assignment_id>/submissions')
@auth.login_required
@auth.teacher_required
def submission_list(course_id, session_id, assignment_id):
    """Returns a page with a list of all submissions for an assignment that
    only the teacher can see"""

    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute('SELECT * FROM sessions WHERE id = %s', (session_id,))

            session = cur.fetchone()

            cur.execute('SELECT * FROM courses WHERE course_num = %s', (session['course_id'],))

            course = cur.fetchone()

            cur.execute('SELECT * FROM assignments WHERE id = %s', (assignment_id,))

            assignment = cur.fetchone()

            cur.execute('SELECT * FROM rosters WHERE session_id = %s', (session['id'],))

            students = cur.fetchall()

    if session == None:

        abort(404)

    if course['teacher_id'] != g.user['id']:

        abort(403)

    if assignment['sessions_id'] != session['id']:

        abort(403)

    for student in students:

        with db.get_db() as con:
            with con.cursor() as cur:

                cur.execute('SELECT * FROM submissions WHERE student_id = %s',
                    (student['user_id'],))

                if cur.fetchone() == None:

                    cur.execute("""INSERT INTO submissions (assignment_id, student_id)
                                   VALUES (%s, %s)""", (assignment['id'], student['user_id'],))


    with db.get_db() as con:
        with con.cursor() as cur:

            # Each submissin has it's id and its student's name
            cur.execute("""SELECT s.id, u.name
                FROM submissions s JOIN users u ON s.student_id = u.id
                WHERE assignment_id = %s""", (assignment['id'],))

            submissions = cur.fetchall()


    return render_template('submissions/submissions.html', submissions=submissions, assignment=assignment, session=session)


@bp.route('/course/<int:course_id>/session/<int:session_id>/assignments/<int:assignment_id>/submissions/<int:submission_id>', methods=('GET', 'POST'))
@auth.login_required
@auth.teacher_required
def grade_submission(course_id, session_id, assignment_id, submission_id):

    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute('SELECT id, course_id FROM sessions WHERE id = %s', (session_id,))

            session = cur.fetchone()

            cur.execute('SELECT teacher_id FROM courses WHERE course_num = %s', (session['course_id'],))

            course = cur.fetchone()

            cur.execute('SELECT * FROM assignments WHERE id = %s', (assignment_id,))

            assignment = cur.fetchone()

            cur.execute('SELECT * FROM submissions WHERE id = %s', (submission_id,))

            submission = cur.fetchone()

            cur.execute('SELECT name FROM users WHERE id = %s', (submission['student_id'],))

            student = cur.fetchone()

    return render_template('submissions/feedback.html', assignment=assignment, student=student['name'], session=session, submission_id=submission_id)
