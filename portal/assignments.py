from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request
)

from portal.db import get_db

bp = Blueprint('assignments', __name__)

@bp.route('/assignments')
def assignments():
    """View for the assignments"""
    course_id = request.args.get('course_id')
    section = request.args.get('section')

    if session['user'][4] == 'student':
    # get the id of the student
        student = session['user'][0]
    # Display the student's assignments
        cur = get_db().cursor()

    # pulls out all assignments for student id
        cur.execute("""SELECT * FROM assignments
                       JOIN student_sessions
                       ON student_sessions_id = student_sessions.id
                       WHERE student_id = %s;""", (student,))
        student_assignments = cur.fetchall()

    if session['user'][4] == 'teacher':
    # Get the id of the student
        teacher = session['user'][0]
    # Display the student's assignments
        cur = get_db().cursor()

    # Pulls out all assignments for student id
        cur.execute("""SELECT * FROM assignments AS a
                       JOIN sessions AS s
                       ON a.course_id = s.course_id AND a.section = s.section
                       WHERE a.course_id = %s;""", (course_id,))
        student_assignments = cur.fetchall()

    return render_template("portal/assignments.html", student_assignments=student_assignments, course_id=course_id, section=section)


@bp.route('/createassignment', methods=("GET", "POST"))
def assignments_create():
    """View for creating an Assignment"""

    if session['user'][4] == 'teacher':  # only if they are a teacher
        if request.method == "POST":
            course_id = request.args.get('course_id')
            section = request.args.get('section')
            name = request.form['name']
            type = request.form['type']
            points = request.form['points']
            duedate = request.form['duedate']

            # MAKE LOOP FOR STUDENT OF STUDENTS SESSIONS
            cur = get_db().cursor()
            cur.execute("""SELECT id FROM student_sessions WHERE course_id = %s AND section = %s;""",
                        (course_id, section))



            student_sessions_id = cur.fetchall()
            for students in student_sessions_id:

                # make a query that inserts into assignments table with this info

                cur.execute("""INSERT INTO assignments (course_id, section, name, type, points, due_date, student_sessions_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s);""", (course_id, section, name, type, points, duedate, students[0]))
                get_db().commit()

            cur.close()

            return redirect(url_for('assignments.assignments', course_id=course_id, section=section))

        return render_template('portal/createassignment.html')
    else:  # if they aren't a teacher return them to home page
        return render_template('portal/home.html')
