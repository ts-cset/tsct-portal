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
    return render_template('layouts/index.html')


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

@bp.route("/session")
def session():
    return render_template("session.html")

@bp.route("/roster", methods= ('GET', 'POST'))
def roster():
    cur = db.get_db().cursor()
    cur.execute(
    "SELECT name"
    " FROM users"
    " ORDER BY name DESC"
    )
    students = cur.fetchall()
    bname = 'boi'

    if request.method == 'POST':
        studentname = request.form['sname']
        for aname in students:
            if aname == studentname:
                cur.execute('SELECT name FROM users WHERE name = %s',(studentname,))
                bname = cur.fetchone()
                cur.close()
    return render_template("roster.html", students=students, bname=bname)
