from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request
)

from portal.db import get_db

bp = Blueprint('courses', __name__)

@bp.route('/courses')
def courses():
    """View for the courses"""
    if session['user'][3] == 'teacher':
    # get the id of the teacher
        teacher = session['user'][0]
    # display the courses they own with a query
        cur = get_db().cursor()

        cur.execute("SELECT * FROM courses WHERE teacher_id = %s;", (teacher,))
        teacher_courses = cur.fetchall()
    else:
        return render_template('portal/home.html')

    return render_template('portal/courses.html', teacher_courses=teacher_courses)

@bp.route('/createcourse', methods=("GET", "POST"))
def courses_create():
    """View for creating a course"""
    if request.method == "POST":
        teacher = session['user'][0]
        cour_name = request.form['cour_name']
        cour_num = request.form['cour_num']
        cour_maj = request.form['cour_maj']
        cour_cred = request.form['cour_cred']

        # make a query that inserts into courses table with this info and teacher id
        cur = get_db().cursor()

        cur.execute("""INSERT INTO courses (major, name, num, credits, teacher_id)
                        VALUES (%s, %s, %s, %s, %s);""", (cour_maj, cour_name, cour_num, cour_cred, teacher))
        get_db().commit()

        return redirect(url_for('courses.courses'))

    return render_template('portal/createcourse.html')

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
