from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@bp.route('/home')
@login_required
@admin
def home():
    return render_template("teacher-home.html")

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
        return render_template("class.html", courses=courses)
    return render_template("CourseCreation.html")


@bp.route('/session', methods=('GET', 'POST'))
@login_required
@admin
def make_session():
    if request.method == "POST":
        course_id = request.form['session']
        session['course_id'] = course_id
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    INSERT INTO sessions (course_id)
                    VALUES (%s);
                    SELECT * FROM sessions
                    WHERE course_id = %s
                    ORDER BY id DESC
                """, (course_id, course_id))

                session['class_session'] = cur.fetchone()

    if session.get('class_session'):
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM courses
                    WHERE id = %s
                """, (session['course_id'],))
                course = cur.fetchone()

                cur.execute("""
                    SELECT * FROM users
                    WHERE major = %s AND role = 'student'
                """, (course['major'],))

                students = cur.fetchall()

                cur.execute("""
                    SELECT u.last_name, u.first_name FROM roster r JOIN users u
                    ON r.student_id = u.id
                    WHERE r.session_id = %s
                """, (session['class_session'][0],))

                roster = cur.fetchall()

        return render_template('create-sessions.html', students=students, roster=roster)
    else:
        return redirect(url_for('teacher.home'))

@bp.route('/session/add', methods=('GET', 'POST'))
@login_required
@admin
def session_add():
    print(session['class_session'])
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                for id in request.form:
                    cur.execute("""
                        INSERT INTO roster (student_id, session_id)
                        VALUES (%s, %s)
                    """, (id, session['class_session'][0]))
    return redirect(url_for('teacher.make_session'))

@bp.route('/session/submit', methods=('GET', 'POST'))
@login_required
@admin
def session_submit():
    if request.method == 'POST':
        session_name = request.form['session_name']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    UPDATE sessions
                    SET session_name = %s
                    WHERE id = %s
                """, (session_name, session['class_session'][0]))
        session.pop('class_session', None)
        session.pop('course_id', None)
    return redirect(url_for('teacher.home'))
