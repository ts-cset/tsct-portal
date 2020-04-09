from flask import Flask, render_template, g, redirect, url_for, Blueprint, request

from . import db

import datetime

bp = Blueprint("college", __name__)


def new_course():
    teacherId = session['user_id']
    major = request.form['major']
    course_name = request.form['new_course']
    course_description = request.form['course_description']
    cur = db.get_db().cursor()
    cur.execute("""
        INSERT INTO courses (name, major, description, teacherId),
        VALUES (%s, %s, %s, %s)""",
                (course_name, major, course_description, teacherId,))
    cur.close()
    cur.commit()


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

    if request.method == 'POST':

        new_course()

        print("new course added")

        return render_template("home.html")


@bp.route("/student")
def student():
    return render_template("student-home.html")
