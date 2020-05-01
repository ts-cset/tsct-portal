from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin, validate, validate_text, validate_number

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@bp.route('/home')
@login_required
@admin
def home():
    """Return a homepage view"""
    return render_template("layouts/teacher/teacher-home.html")

@bp.route('/courses', methods=('GET', 'POST'))
@login_required
@admin
def courses():
    """Return a view that contains course information that can be deleted on POST"""
    if request.method == 'POST':

        ids =[]
        error = None

        # Get all ids from checked boxes and validate them
        for id in request.form.getlist('id'):
            if validate(id, 'courses'):
                ids.append(int(id))
            else:
                # If any id fails validation, set an error and stop looping
                error = "Something went wrong."
                break

        if not error:
            # If the validation went through, open a database connection and delete
            # the selected courses
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM courses
                        WHERE id = ANY(%s)
                    """, (ids,))
        else:
            # If the validation produced an error, prepare it to be shown to the user
            flash(error)

    # Open a DB connection and grab all the course information for logged in teacher
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
def create():
    """Create a class with user input as data"""
    if request.method == "POST":
        # Requests tags with 'code', 'name', 'major', and 'description' in form
        class_code = request.form['code']
        class_name = request.form['name']
        class_subject = request.form['major']
        class_description = request.form['description']

        if (
            validate_number(class_code, 999) and
            validate_text(class_name, 50) and
            validate_text(class_subject, 5) and
            validate_text(class_description, 150)
        ):
            # Inserts data into database if all validation passes
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses(course_code, course_name, major, description, teacher_id ) VALUES(%s, %s, %s, %s, %s)",
                    (class_code, class_name, class_subject, class_description, g.user['id'], )
                    )
            return redirect(url_for('teacher.courses'))
        else:
            # If validation fails, prepare an error to be shown to the user
            flash("Something went wrong.")

    return render_template('layouts/teacher/courses/course-creation.html')

@bp.route('/courses/<int:id>/edit', methods=('POST', 'GET'))
@login_required
@admin
def course_edit(id):
    """Update course information using user input as data"""
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
                # If all data is successfully validated, update the DB
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
                # If validation fails, prepare an error to be shown to the user
                flash("Something went wrong.")

        # Grab the current course information so the user knows what they're changing
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM courses
                    WHERE id = %s
                """, (id,))
                course = cur.fetchone()

        return render_template('layouts/teacher/courses/edit-course.html', course=course)

    return redirect(url_for('teacher.courses'))
