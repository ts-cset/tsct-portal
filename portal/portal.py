from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session
from . import db

bp = Blueprint("portal", __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/home", methods=['GET', 'POST'])
def home():

    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses""")
    courses = cur.fetchall()
    cur.close()
    print(courses)

    return render_template("home.html", courses=courses)


@bp.route("/<int:id>/edit", methods=('GET', 'POST'))
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
        course_name = request.form['new_course']
        course_description = request.form['course_description']

        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE courses SET name = %s, description = %s, teacherId = %s'
            ' WHERE course_id = %s ',
            (course_name, course_description, teacherId, id)
        )
        g.db.commit()
        cur.close()

        return redirect(url_for('portal.home'))

    return render_template("layouts/courses/edit.html", course=course)


@bp.route("/<int:id>/delete", methods=["POST", ])
def delete(id):
    """delete unwanted tasks"""
    cur = db.get_db().cursor()

    cur.execute(
        'DELETE FROM courses WHERE course_id= %s', (id,)
    )
    g.db.commit()
    cur.close()
    return redirect(url_for('portal.home'))


@bp.route("/student")
def student():
    return render_template("student-home.html")


@bp.route("/create", methods=['GET', 'POST'])
def create():

    cur = db.get_db().cursor()
    cur.execute("""
        SELECT major_id, name FROM majors""",
                )
    majors = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        teacherId = session['user_id']
        major = request.form['majors']
        course_name = request.form['new_course']
        course_description = request.form['course_description']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO courses (name, major, description, teacherId)
        VALUES (%s, %s, %s, %s)""",
                    (course_name, major, course_description, teacherId,))

        g.db.commit()
        return redirect(url_for('portal.home'))

    return render_template("layouts/courses/create_courses.html", majors=majors)
