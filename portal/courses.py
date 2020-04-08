from flask import (
    Blueprint, g, render_template, redirect, url_for, session
)

from portal.db import get_db

bp = Blueprint('courses', __name__)

@bp.route('/courses')
def courses():
    if session['user'][3] == 'teacher':
    # get the id of the teacher
        teacher = session['user'][0]
        print(teacher)
    # display the courses they own with a query
        cur = get_db().cursor()

        cur.execute("SELECT * FROM courses WHERE teacher_id = %s;", (teacher,))
        teacher_courses = cur.fetchall()
        print(teacher_courses)

    return render_template('portal/courses.html', teacher_courses=teacher_courses)

@bp.route('/courses/createcourse', methods=("POST",))
def courses_create():
    return redirect(url_for('courses.courses'))

@bp.route('/editcourse', methods=("GET", "POST"))
def courses_edit():
    """Edits the course name/info"""
    cur = get_db().cursor()
    if request.method == "POST":
        new = request.form['new']

        if not new:


            return render_template('portal/editcourse.html')
            # Update the task
        else:
            cur.execute(
                'UPDATE course SET description = %s'
                'WHERE id = %s ',
                (new, id)
            )
            get_db().commit()
            cur.close()

        return redirect(url_for('editcourse.course'))
    return render_template("portal/editcourse.html")
