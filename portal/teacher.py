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
@login_required
@admin
def courses():
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                for item in request.form:
                    cur.execute("""
                        DELETE FROM courses
                        WHERE id = %s
                    """, (request.form[item],))

    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT * FROM courses
                WHERE teacher_id = %s
            """, (g.user['id'],))
            courses = cur.fetchall()
    return render_template('class.html', courses=courses)

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
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO courses(course_code, course_name, major, description, teacher_id ) VALUES(%s, %s, %s, %s, %s)",
                (class_code, class_name, class_subject, class_description, g.user['id'], )
                )
        #Selects all the data from courses and returns it to 'class.html'
        return redirect(url_for('teacher.courses'))
    return render_template('course-creation.html')


@bp.route('/session/create', methods=('GET', 'POST'))
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

                session_id = cur.fetchone().get('id')
                session['class_session'] = session_id

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
                """, (session['class_session'],))

                roster = cur.fetchall()

        return render_template('create-sessions.html', students=students, roster=roster)
    else:
        return redirect(url_for('teacher.home'))

@bp.route('/session/add', methods=('GET', 'POST'))
@login_required
@admin
def session_add():
    if request.method == 'POST':
        if session.get('class_session'):
            with db.get_db() as con:
                with con.cursor() as cur:
                    for id in request.form:
                        cur.execute("""
                            INSERT INTO roster (student_id, session_id)
                            VALUES (%s, %s)
                        """, (id, session['class_session']))
    return redirect(url_for('teacher.make_session'))

@bp.route('/session/submit', methods=('GET', 'POST'))
@login_required
@admin
def session_submit():
    if request.method == 'POST':
        if session.get('class_session'):
            session_name = request.form['session_name']
            meeting_days = request.form['meeting_days']
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        UPDATE sessions
                        SET session_name = %s, meeting_days = %s
                        WHERE id = %s
                    """, (session_name, meeting_days, session['class_session']))
            session.pop('class_session', None)
            session.pop('course_id', None)
            return redirect(url_for('teacher.home'))
    return redirect(url_for('teacher.make_session'))

@bp.route('/session/cancel')
@login_required
@admin
def session_cancel():
    if session.get('class_session'):
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    DELETE FROM roster
                    WHERE session_id = %s
                """, (session['class_session'],))
                cur.execute("""
                    DELETE FROM sessions
                    WHERE id = %s
                """, (session['class_session'],))
        session.pop('class_session', None)
        session.pop('course_id', None)
    return redirect(url_for('teacher.home'))
