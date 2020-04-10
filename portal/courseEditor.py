from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash

from . import db

bp = Blueprint("courseEditor", __name__)


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
    """Allows the teacher to create a course
    and fill out specifics on course"""
    majorChoices = get_majors()

    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                courseTitle = request.form['courseTitle']
                courseDescription = request.form['description']
                courseCredit = request.form['courseCredits']
                courseMajor = request.form['major_name']
                error = None

                if not courseTitle:
                    error = 'You are missing a required field'
                if not courseCredit:
                    error = 'You are missing a required field'
                if not courseDescription:
                    error = 'You are missing a required field'
                if not courseMajor:
                    error = 'You are missing a required field'
                # Adds info to courses table
                cur.execute("""INSERT INTO courses (course_title, description,
                credits)
                VALUES (%s, %s, %s)""",
                            (courseTitle, courseDescription,
                             courseCredit,)
                            )
                con.commit()
                # Adds info to majors table
                cur.execute("""INSERT INTO majors (name)
                VALUES (%s)""",
                            (courseMajor,)
                            )
                con.commit()

                return redirect(url_for("courseEditor.course_manage"))

            flash(error)

    return render_template('layouts/courseCreate.html', majorChoices=majorChoices)

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM courses')
    course = cur.fetchall()
    cur.close()
    return render_template("layouts/courseCreate.html")


# Needs new template
@bp.route("/courseEdit/<int:id>", methods=('GET', 'POST'))
def course_edit(id):
    """Allows user to edit the course"""
    course = get_course(id)

    if request.method == "POST":

        credit = request.form['editCredit']
        title = request.form['editTitle']
        desc = request.form['editDesc']
        error = None
        with db.get_db() as con:
            with con.cursor() as cur:

                if not credit:
                    error = 'All fields must be filled in to edit course.'
                if not title:
                    error = 'All fields must be filled in to edit course.'
                if not desc:
                    error = 'All fields must be filled in to edit course.'

                if error is None:

                    cur.execute("""UPDATE courses SET
                    course_title = %s,
                    description = %s,
                    credits = %s
                    WHERE course_num = %s
                    """,
                                (title, desc, credit, id)
                                )
                    con.commit()

                    return redirect(url_for("courseEditor.course_manage"))

                flash(error)

    return render_template("layouts/courseEdit.html", course=course)


def get_course(id):
    """Gets the course from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
                'SELECT course_num, credits, description, course_title'
                ' FROM courses WHERE course_num = %s',
                (id,))

            course = cur.fetchone()

            if course is None:
                abort(404, "Course id {0} doesn't exist.".format(id))

            return course


def get_majors():
    """Gets the list of majors"""
    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
                'SELECT name '
                'FROM majors'
            )

            majorChoices = cur.fetchall()
            print(majorChoices)

            return majorChoices
