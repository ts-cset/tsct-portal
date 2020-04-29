from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('assignments', __name__, url_prefix='/portal/assignments')

@bp.route('/<course_id>/<session_id>/view-assignment/<assignment_id>', methods=('GET', 'POST'))
@login_required
def view_assignment(course_id, session_id, assignment_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM session
                   WHERE id = %s;""",
                   (session_id,))
    sessions = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE id = %s;""",
                   (assignment_id,))
    assignments = cur.fetchall()
    if g.users['role'] == 'teacher':
        cur.execute("""SELECT grades.letter, submissions.* FROM submissions
                       JOIN grades ON submissions.grades_id = grades.id
                       WHERE assignments_id = %s;""",
                       (assignment_id,))
        submissions = cur.fetchall()

        cur.execute("""SELECT users.id, users.email, users.name, roster.users_id FROM roster
                        JOIN users ON users.id= roster.users_id
                        WHERE roster.session_id = %s;""",
                    (session_id,))
        students = cur.fetchall()


    else:
        cur.execute("""SELECT grades.letter, submissions.* FROM submissions
                       JOIN grades ON submissions.grades_id = grades.id
                       WHERE assignments_id = %s and users_id = %s;""",
                       (assignment_id, g.users['id']))
        submissions = cur.fetchall()
        cur.close()
        return render_template('portal/courses/sessions/assignments/view-assignment.html', courses=courses, sessions=sessions, assignments=assignments, submissions=submissions)
    return render_template('portal/courses/sessions/assignments/view-assignment.html', courses=courses, sessions=sessions, assignments=assignments, submissions=submissions, students=students)

@bp.route('<assignment_id>/submit-assignment', methods=('GET', 'POST'))
@login_required
def submit_assignment(assignment_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE id = %s;""",
                   (assignment_id,))
    assignments = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        answer = request.form['answer']
        error = None
        cur = db.get_db().cursor()
        try:
            cur.execute("""
            UPDATE submissions SET answer = %s
            WHERE users_id = %s and assignments_id = %s;""",
            (answer, g.users['id'], assignment_id))
            db.get_db().commit()
        except:
            error = "There was a problem with this submission"
            return render_template('error.html', error=error)
        else:
            #where i need go add going back to the view assignments
            return redirect(url_for('portal.userpage'))
    return render_template('portal/courses/sessions/assignments/submit-assignments.html', assignments=assignments)

@bp.route('/<session_id>/create-assignment', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_assignment(session_id):

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        points = request.form['points']
        description = request.form['description']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM assignments
        WHERE name = %s and session_id = %s;
        """,
        (name, session_id))
        assignment = cur.fetchone()

        if assignment != None:
            error = "That assignment already exists"
        flash(error)

        if error is None:
            try:
                cur.execute("""INSERT INTO assignments (session_id, name, date, description, points)
                VALUES (%s, %s, %s, %s, %s);
                 """,
                 (session_id, name, date, description, points))
                db.get_db().commit()
            except:
                error = "There was a problem creating that assignment"
                flash(error)

            else:
                cur.execute("""
                SELECT id FROM assignments
                WHERE name = %s and session_id = %s;
                """,
                (name, session_id))
                assignments = cur.fetchone()
                assignment_id = assignments[0]
                cur.execute("""
                SELECT users.id FROM users
                JOIN roster ON roster.users_id = users.id
                JOIN session ON session.id = roster.session_id
                WHERE session_id = %s;
                """,
                (session_id,))
                students = cur.fetchall()
                for student in students:
                    cur.execute("""INSERT INTO submissions (users_id, assignments_id)
                    VALUES (%s, %s);
                     """,
                     (student[0], assignment_id))
                    db.get_db().commit()


                cur.execute("""SELECT session.courses_id FROM courses
                           JOIN session ON session.courses_id = courses_id
                           Where session.id = %s;""",
                           (session_id,))
                courses = cur.fetchone()
                course_id = courses[0]
                print('course id HI IM RIGHT HERE GOD DAMN IT', course_id)


                cur.execute("""
                SELECT id FROM assignments
                WHERE name = %s and session_id = %s;
                """,
                (name, session_id))
                assignments = cur.fetchone()
                assignment_id = assignments[0]

                cur.close()

                return redirect(url_for('assignments.view_assignment', course_id=course_id, session_id=session_id, assignment_id=assignment_id))
        else:
            return redirect(url_for('assignments.create_assignment', session_id=session_id))
    return render_template('portal/courses/sessions/assignments/create-assignments.html')

@bp.route('<course_id>/<session_id>/grade-assignment/<assignment_id>', methods=('GET', 'POST'))
@login_required
@teacher_required
def grade_assignment(course_id, session_id, assignment_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM session
                   WHERE id = %s;""",
                   (session_id,))
    sessions = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE id = %s;""",
                   (assignment_id,))
    assignments = cur.fetchall()
    cur.execute("""SELECT * FROM submissions
                   WHERE assignments_id = %s;""",
                   (assignment_id,))
    submissions = cur.fetchall()

    cur.execute("""SELECT users.id, users.email, users.name, roster.users_id FROM roster
                        JOIN users ON users.id= roster.users_id
                        WHERE roster.session_id = %s;""",
                    (session_id,))
    students = cur.fetchall()

    cur.close()

    if request.method == 'POST':
        points = request.form.getlist('points')
        count = 0
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT points FROM assignments
        WHERE id = %s;
        """,
        (assignment_id,))
        assignment = cur.fetchone()
        assignment_point = assignment[0]

        cur.execute("""
        SELECT users.id, submissions.users_id, session.id, assignments.* FROM submissions
        JOIN users ON users.id = submissions.users_id
		JOIN assignments ON assignments.id = submissions.assignments_id
		JOIN session ON session.id = assignments.session_id
        WHERE assignments.id = %s
        """,
        (assignment_id,))
        users = cur.fetchall()

        for user in users:
            print(points[count])
            points[count] = float(points[count])

            if points[count] > assignment_point or points[count] < 0:
                error = "Invalid point amount"
            flash(error)

            if error is None:
                grade = (points[count]/assignment_point)

                if grade >= 0.98:
                    grade_id = 1
                elif grade >= 0.93:
                    grade_id = 2
                elif grade >= 0.90:
                    grade_id = 3
                elif grade >= 0.87:
                    grade_id = 4
                elif grade >= 0.83:
                    grade_id = 5
                elif grade >= 0.80:
                    grade_id = 6
                elif grade >= 0.77:
                    grade_id = 7
                elif grade >= 0.73:
                    grade_id = 8
                elif grade >= 0.70:
                    grade_id = 9
                elif grade >= 0.67:
                    grade_id = 10
                elif grade >= 0.63:
                    grade_id = 11
                elif grade >= 0.60:
                    grade_id = 12
                else:
                    grade_id = 13

                cur.execute("""UPDATE submissions SET points = %s, grades_id = %s
                WHERE users_id = %s and assignments_id = %s;
                 """,
                 (points[count], grade_id, user[0], assignment_id))
                db.get_db().commit()
                count += 1

                return redirect(url_for('portal.userpage'))

    return render_template('portal/courses/sessions/assignments/grade-assignments.html', courses=courses, sessions=sessions, assignments=assignments, submissions=submissions, students=students)

@bp.route('/<route>')
@login_required
def error(route=None):
    error = "404 Not found"
    return render_template('error.html', error=error)
