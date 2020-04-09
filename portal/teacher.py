from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@bp.route('/courses', methods=('GET', 'POST'))
#Checks if the user is log in and if they are an admin role
@login_required
@admin
#Creates class
def courses():
    if request.method == "POST":
        #Requests tags with 'code', 'name', 'major', and 'description' in form
        class_code = request.form['code']
        class_name = request.form['name']
        class_subject = request.form['major']
        class_description = request.form['description']
        #Inserts data into database
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO courses(course_code, course_name, major, description, teacher_id ) VALUES(%s, %s, %s, %s, %s)",
                (class_code, class_name, class_subject, class_description, g.user['id'], )
                )
        #Selects all the data from courses and returns it to 'class.html'
        cur = db.get_db().cursor()
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        cur.close()
        return render_template("layouts/class.html", courses=courses)
    return render_template("layouts/CourseCreation.html")
