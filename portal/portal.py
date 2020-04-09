from flask import redirect, g, url_for, render_template, session, request, Blueprint

from . import db

bp = Blueprint("portal", __name__)


@bp.route("/courseManagement", methods=('GET', 'POST'))  # Management Page
def course_manage():
    """Allows teachers to have a page which allows
    them to edit and create courses"""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM courses')
    course = cur.fetchall()
    cur.close()
    return render_template("layouts/courseMan.html", course=course)


@bp.route("/courseCreate", methods=('GET', 'POST'))  # Course Create
def course_create():
    """Allows the teacher to create a course and fill out specifics on course"""
    # if request.method == 'POST':
    #     with get_db() as con:
    #         with con.cursor() as cur:
    #             courseTitle = request.form['courseTitle']
    #             couresDescription = request.form['courseDescription']
    #             couresCredit = request.form['courseCredits']
    #             courseTeacher = request.form['courseTeachers']
    #             courseMajor = request.form['courseMajor']
    #
    #             if not courseTitle or courseCredit or courseTeacher or courseMajor:
    #                 error = 'You are missing a required field'  # Mark required field with *
    #
    #             if error is not None:
    #                 flash(error)
    #
    #             cur.execute("""INSERT INTO courses (course_title, description,
    #             credit, teacher_name, major_name)
    #             VALUES (?, ?, ?, ?, ?)""",
    #                         (courseTitle, courseDescription,
    #                          courseCredit, courseTeacher, courseMajor)
    #                         )
    #             con.commit()
    #             return redirect(url_for('layouts.courseMan.html'))
    #
    #     return render_template('layouts.courseCreate.html')
    #
    # cur = db.get_db().cursor()
    # cur.execute('SELECT * FROM courses')
    # course = cur.fetchall()
    # cur.close()
    return render_template("layouts/courseCreate.html")


# Needs new template
@bp.route("/courseEdit/<int:id>", methods=('GET', 'POST'))
def course_edit(id):
    """Allows user to edit the course"""
    course = get_course(id)

    # con = get_db()
    # cur = con.cursor()

    return render_template("layouts/courseEdit.html", course=course)


# Needs new template
# @bp.route("/courseInfo/<int:id>", methods=('GET', 'POST'))
# def course_info(id):
#     """Allows teachers to see current info on a course they own"""
#
#   return render_template("layouts/courseInfo.html")


def get_course(id):
     # Gets the course id (in progress)
     cur = db.get_db().cursor()
    course = cur.get_db().execute(
        'SELECT c.course_num, email, full_name, c.teacher_name'
        ' FROM courses c JOIN user u ON c.teacher_name = u.full_name'
        ' WHERE c.course_num = ?',
        (id,)

    ).fetchone()

    if course is None:
        abort(404, "Course id {0} doesn't exist.".format(id))

    return course
