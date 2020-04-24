from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request, flash
)

from portal.db import get_db

bp = Blueprint('courses', __name__)

# ------- Course Page -----------------------------------------------------------------
@bp.route('/courses')
def courses():
    """View for the courses"""
    if session['user'][4] == 'teacher':  # only if they are a teacher
        # get the id of the teacher
        teacher = session['user'][0]
    # display the courses they own with a query
        cur = get_db().cursor()

        cur.execute("SELECT * FROM courses WHERE teacher_id = %s;", (teacher,))
        teacher_courses = cur.fetchall()

        return render_template('portal/courses.html', teacher_courses=teacher_courses)
    else:  # if not a teacher, return to home page
        return render_template('portal/home.html')


# ------- Create Courses -----------------------------------------------------------------
@bp.route('/createcourse', methods=("GET", "POST"))
def courses_create():
    """View for creating a course"""
    if session['user'][4] == 'teacher':  # only if they are a teacher
        if request.method == "POST":
            teacher = session['user'][0]
            cour_name = request.form['cour_name']
            cour_num = request.form['cour_num']
            cour_maj = request.form['cour_maj']
            cour_cred = request.form['cour_cred']
            cour_desc = request.form['cour_desc']
            # checks major name length
            if len(cour_maj) > 4:
                error = 'course major name can only be 4 letters'
                flash(error)
                return render_template('portal/createcourse.html')
            # make a query that inserts into courses table with this info and teacher id
            cur = get_db().cursor()
            cur.execute("SELECT * FROM courses WHERE name = %s;", (cour_name,))
            existingcourse = cur.fetchall()
            print('print')
            print(existingcourse)
            if existingcourse != []:
                error = "Name already exists"
                # TODO: don't clear user data
                session['cour_name'] = cour_name
                session['cour_num'] = cour_num
                session['cour_maj'] = cour_maj
                session['cour_cred'] = cour_cred
                session['cour_desc'] = cour_desc
                flash(error)
                return render_template('portal/createcourse.html')
            cur.execute("""INSERT INTO courses (major, name, num, description, credits, teacher_id)
                            VALUES (%s, %s, %s, %s, %s, %s);""", (cour_maj, cour_name, cour_num, cour_desc, cour_cred, teacher))
            session['cour_name'] = ''
            session['cour_num'] = ''
            session['cour_maj'] = ''
            session['cour_cred'] = ''
            session['cour_desc'] = ''
            get_db().commit()
            cur.close()

            return redirect(url_for('courses.courses'))

        return render_template('portal/createcourse.html')
    else:  # if they aren't a teacher return them to home page
        return render_template('portal/home.html')


@bp.route('/<int:cour_id>/viewcourse')
def courses_view(cour_id):
    """Shows details of a course to teacher"""
    if session['user'][4] == 'teacher':  # if they are a teacher
        teacher = session['user'][0]
        cur = get_db().cursor()

        cur.execute(
            "SELECT * FROM courses WHERE teacher_id = %s AND id = %s;", (teacher, cour_id))

        course = cur.fetchone()
        return render_template('portal/viewcourse.html', course=course)
    else:  # if not a teacher, send to home
        return render_template('portal/home.html')


@bp.route('/deletecourse', methods=("POST",))
def courses_delete():
    """View for deleting courses"""
    if session['user'][4] == 'teacher':  # if the are a teacher
        course_to_delete = request.form['course_to_delete']
        teacher = session['user'][0]
        cur = get_db().cursor()

        cur.execute("DELETE FROM courses WHERE teacher_id = %s AND id = %s;",
                    (teacher, course_to_delete))
        get_db().commit()
        cur.close()
        return redirect(url_for('courses.courses'))
    else:  # if not a teacher, send to home
        return render_template('portal/home.html')


# ------- Edit Courses -----------------------------------------------------------------
@bp.route('/<int:cour_id>/editcourse', methods=("GET", "POST"))
def courses_edit(cour_id):
    """Edits the course name/info"""
    cur = get_db().cursor()
    teacher = session['user'][0]
    cur.execute("SELECT * FROM courses WHERE teacher_id = %s AND id = %s;",
                (teacher, cour_id))
    course = cur.fetchone()

    if session['user'][4] == 'teacher':

        if request.method == "POST":
            error = None
            cour_name = request.form['cour_name']
            cour_num = request.form['cour_num']
            cour_maj = request.form['cour_maj']
            cour_cred = request.form['cour_cred']
            cour_desc = request.form['cour_desc']

            if len(cour_maj) > 4:
                error = 'course major name can only be 4 letters'
                flash(error)
                return render_template("portal/editcourse.html", course=course)

            cur.execute(
                "SELECT * FROM courses WHERE name = %s and id != %s;", (cour_name, cour_id))
            existingcourse = cur.fetchall()
            print('print')
            print(existingcourse)
            if existingcourse != []:
                error = "Name already exists"
                # TODO: don't clear user data
                session['cour_name'] = cour_name
                session['cour_num'] = cour_num
                session['cour_maj'] = cour_maj
                session['cour_cred'] = cour_cred
                session['cour_desc'] = cour_desc
                flash(error)
                return render_template('portal/createcourse.html')

            # Update the course
            cur.execute(
                """UPDATE courses SET (major, name, num, credits, description) = (%s, %s, %s, %s, %s)
                    WHERE id = %s AND teacher_id = %s ;""", (cour_maj, cour_name, cour_num, cour_cred, cour_desc, cour_id, teacher)
            )
            session['cour_name'] = ''
            session['cour_num'] = ''
            session['cour_maj'] = ''
            session['cour_cred'] = ''
            session['cour_desc'] = ''
            get_db().commit()
            cur.close()

            return redirect(url_for('courses.courses'))

        return render_template("portal/editcourse.html", course=course)
    else:  # if not a teacher, send them to home page
        return render_template('portal/home.html')
