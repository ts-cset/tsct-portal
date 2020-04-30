from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin, validate, validate_text, validate_number

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@bp.route('/home')
@login_required
@admin
def home():
    return render_template("layouts/teacher/teacher-home.html")

@bp.route('/courses', methods=('GET', 'POST'))
@login_required
@admin
def courses():
    if request.method == 'POST':

        ids =[]
        error = None

        for id in request.form.getlist('id'):
            if validate(id, 'courses'):
                ids.append(int(id))
            else:
                error = "Something went wrong."
                break

        if not error:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM courses
                        WHERE id = ANY(%s)
                    """, (ids,))
        else:
            flash(error)

    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT * FROM courses
                WHERE teacher_id = %s
            """, (g.user['id'],))
            courses = cur.fetchall()
    return render_template('layouts/teacher/courses/courses.html', courses=courses)

@bp.route('/courses/create', methods=('GET', 'POST'))
#Checks if the user is log in and if they are an admin role
@login_required
@admin
#Creates class
def create():
    if request.method == "POST":
        #Requests tags with 'code', 'name', 'major', and 'description' in form
        class_code = request.form['code']
        class_name = request.form['name']
        class_subject = request.form['major']
        class_description = request.form['description']
        #Inserts data into database
        if (
            validate_number(class_code, 999) and
            validate_text(class_name, 50) and
            validate_text(class_subject, 5) and
            validate_text(class_description, 150)
        ):
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses(course_code, course_name, major, description, teacher_id ) VALUES(%s, %s, %s, %s, %s)",
                    (class_code, class_name, class_subject, class_description, g.user['id'], )
                    )
            return redirect(url_for('teacher.courses'))
        else:
            flash("Something went wrong.")

    return render_template('layouts/teacher/courses/course-creation.html')

@bp.route('/courses/<int:id>/edit', methods=('POST', 'GET'))
@login_required
@admin
def course_edit(id):
    if validate(id, 'courses'):
        if request.method == "POST":
            class_code = request.form['code']
            class_name = request.form['name']
            class_subject = request.form['major']
            class_description = request.form['description']
            if (
                validate_text(class_code, 10) and
                validate_text(class_name, 50) and
                validate_text(class_subject, 5) and
                validate_text(class_description, 150)
            ):
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                        UPDATE courses
                        SET course_code = %s, course_name = %s , major= %s, description= %s, teacher_id= %s
                        WHERE id = %s
                        """,
                        (class_code, class_name, class_subject, class_description, g.user['id'], id)
                        )
                return redirect(url_for('teacher.courses'))
            else:
                flash("Something went wrong.")

        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM courses
                    WHERE id = %s
                """, (id,))
                course = cur.fetchone()

        return render_template('layouts/teacher/courses/edit-course.html', course=course)

    return redirect(url_for('teacher.courses'))
