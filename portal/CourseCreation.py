from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin

bp = Blueprint('CourseCreation', __name__)

@bp.route('/ClassCreation', methods=('GET', 'POST'))
#Checks if the user is log in and if they are an admin role
@login_required
@admin
#Creates class
def classCreation():
    if request.method == "POST":
        #Requests tags with 'Class-Name', 'Class-Major', and 'Class-description' in form
        className = request.form['Class-Name']
        classSubject = request.form['Class-Major']
        classDescription = request.form['description']
        #Inserts data into database
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO courses(course_code, course_name, major, description, teacher_id ) VALUES(%s, %s, %s, %s, %s)",
                (50, className, classSubject, classDescription, g.user['id'], )
                )
        #Selects all the data from courses and returns it to 'class.html'
        cur = db.get_db().cursor()
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        cur.close()
        return render_template("Class.html", courses=courses)
    return render_template("CourseCreation.html")
