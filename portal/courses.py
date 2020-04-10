from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request
)

from portal.db import get_db

bp = Blueprint('courses', __name__)

@bp.route('/courses')
def courses():
    """View for the courses"""
    if session['user'][4] == 'teacher':
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
    if session['user'][4] == 'teacher':
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
            cur.close()

            return redirect(url_for('courses.courses'))

        return render_template('portal/createcourse.html')
@bp.route('/<int:cour_id>/viewcourse')
def courses_view(cour_id):
    """Shows details of a course to teacher"""
    if session['user'][4] == 'teacher':
        teacher = session['user'][0]
        cur = get_db().cursor()

        cur.execute("SELECT * FROM courses WHERE teacher_id = %s AND id = %s;", (teacher, cour_id))

        course = cur.fetchone()
        return render_template('portal/viewcourse.html', course=course)
    else:
        return render_template('portal/home.html')

@bp.route('/deletecourse', methods=("POST",))
def courses_delete():
    """View for deleting courses"""
    if session['user'][4] == 'teacher':
        if request.method == 'POST':
            course_to_delete = request.form['course_to_delete']
            teacher = session['user'][0]
            cur = get_db().cursor()

            cur.execute("DELETE FROM courses WHERE teacher_id = %s AND id = %s;", (teacher, course_to_delete))
            get_db().commit()
            cur.close()
            return redirect(url_for('courses.courses'))

@bp.route('/<int:cour_id>/editcourse', methods=("GET", "POST"))
def courses_edit(cour_id):
    """Edits the course name/info"""
    if session['user'][4] == 'teacher':
        cur = get_db().cursor()
        if request.method == "POST":
            cour_name = request.form['cour_name']
            cour_num = request.form['cour_num']
            cour_maj = request.form['cour_maj']
            cour_cred = request.form['cour_cred']
            cour_desc = request.form['cour_desc']

                # Update the task
            cur.execute(
                    """UPDATE courses SET (major, name, num, credits, description) = (%s, %s, %s, %s, %s)
                    WHERE id = %s;""", (cour_maj, cour_name, cour_num, cour_cred, cour_desc , cour_id)
                )
            get_db().commit()
            cur.close()

            return redirect(url_for('courses.courses'))
        return render_template("portal/editcourse.html")
