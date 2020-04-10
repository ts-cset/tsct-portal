from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session
from . import db
bp = Blueprint("portal", __name__)


def new_course():
    teacherId = session['user_id']
    major = request.form['major']
    course_name = request.form['new_course']
    course_description = request.form['course_description']
    cur = db.get_db().cursor()
    cur.execute("""
        INSERT INTO courses (name, major, description, teacherId)
        VALUES (%s, %s, %s, %s)""",
                (course_name, major, course_description, teacherId,))
    g.db.commit()

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/home", methods=['GET', 'POST'])
def home():
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses""")
    courses = cur.fetchall()
    cur.close()



    if request.method == 'POST':

        new_course()
        cur = db.get_db().cursor()
        cur.execute("""SELECT * FROM courses""")
        courses = cur.fetchall()
        cur.close()

        return render_template("home.html", courses=courses, majors=majors)

    return render_template("home.html", courses=courses, majors=majors)


@bp.route("/<int:id>/edit", methods=('GET','POST'))
def edit(id):
    """Edits the description of the courses"""
    cur = db.get_db().cursor()
    cur.execute(
        'SELECT * from courses WHERE course_id=%s',
        (id,)
    )
    course = cur.fetchone()

    if request.method == 'POST':

        teacherId = session['user_id']
        major = request.form['major']
        course_name = request.form['new_course']
        course_description = request.form['course_description']

        cur = db.get_db().cursor()
        cur.execute(
                'UPDATE courses SET name = %s, major = %s, description = %s, teacherId = %s'
                ' WHERE course_id = %s ',
                (course_name, major, course_description, teacherId, id)
            )
        g.db.commit()
        cur.close()

        return redirect(url_for('portal.home'))

    return render_template("edit.html", course=course)

@bp.route("/student")
def student():
    return render_template("student-home.html")
