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
    cur.close()


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/home", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        new_course()

        print("new course added")

        return render_template("home.html")

    return render_template("home.html")


@bp.route("/student")
def student():
    return render_template("student-home.html")
