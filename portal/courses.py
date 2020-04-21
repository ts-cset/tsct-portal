from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('courses', __name__, url_prefix='/portal/courses')

@bp.route('/')
@login_required
def courses():
    cur = db.get_db().cursor()
    if g.users['role'] == "teacher":
        cur.execute("""SELECT * FROM courses""")
        courses = cur.fetchall()
        cur.close()
    else:
        cur.execute("""
            SELECT DISTINCT ON (courses.id) roster.*, users.*, session.*, courses.* FROM roster
            JOIN users ON users.id = roster.users_id
            JOIN session ON session.id = roster.session_id
            JOIN courses ON courses.id = session.courses_id
            WHERE users.id = %s;""",
            (g.users['id'],))
        courses = cur.fetchall()
        cur.close()
    return render_template('portal/courses/index.html', courses=courses)

@bp.route('/view-course/<course_id>', methods=('GET', 'POST'))
@login_required
def view_course(course_id):
    cur = db.get_db().cursor()
    if g.users['role'] == "teacher":
        cur.execute("""SELECT * FROM courses
                       WHERE id = %s;""",
                       (course_id,))
        courses = cur.fetchall()
        cur.execute("""SELECT * FROM session
                       WHERE courses_id = %s;""",
                       (course_id,))
        sessions = cur.fetchall()
        cur.close()
    else:
        cur.execute("""
            SELECT DISTINCT ON (courses.id) courses.*, roster.id AS r_id, users.id AS u_id, session.id AS s_id FROM roster
            JOIN users ON users.id = roster.users_id
            JOIN session ON session.id = roster.session_id
            JOIN courses ON courses.id = session.courses_id
            WHERE users.id = %s and courses_id = %s;""",
            (g.users['id'], course_id))
        courses = cur.fetchall()
        cur.execute("""
            SELECT DISTINCT ON (session.id) session.*, roster.id AS r_id, users.id AS u_id, courses.id AS c_id FROM roster
            JOIN users ON users.id = roster.users_id
            JOIN session ON session.id = roster.session_id
            JOIN courses ON courses.id = session.courses_id
            WHERE users.id = %s and courses_id = %s;""",
            (g.users['id'], course_id))
        sessions = cur.fetchall()
        print(sessions)
        cur.close()
    return render_template('portal/courses/view-course.html', courses=courses, sessions=sessions)

@bp.route('/create-course', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_course():
    if request.method == 'POST':
        course_number = request.form['course_number']
        name = request.form['name']
        description = request.form['description']
        credits = request.form['credits']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM courses
        WHERE course_number = %s and name = %s;
        """,
        (course_number, name))
        courses = cur.fetchone()

        if courses != None:
            error = "That course already exists"

        if error is None:
            cur.execute("""
             INSERT INTO courses (course_number, major, name, description, credits, teacher)
             VALUES (%s, %s, %s, %s, %s, %s);
             """,
             (course_number, g.users['major'], name, description, credits, g.users['id']))
            db.get_db().commit()
            cur.close()


            #routing 
            cur.execute("""
            SELECT id FROM courses WHERE id = %s;
            """),
            (id,)
            courses = cur.fetchone()
            course_id = courses[0]

            cur.execute("""SELECT id FROM session
            WHERE name = %s and courses_id = %s;
            """,
            (name, course_id))
            sessions = cur.fetchone()
            session_id = sessions[0]
            cur.close()




            return redirect(url_for('portal.userpage'))

    return render_template('portal/courses/create-course.html')

@bp.route('/update-course/<course_id>', methods=('GET', 'POST'))
@login_required
@teacher_required
def update_course(course_id):
    if request.method == 'POST':
        course_number = request.form['course_number']
        name = request.form['name']
        description = request.form['description']
        credits = request.form['credits']
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM courses
        WHERE course_number = %s and name = %s;
        """,
        (course_number, name))
        courses = cur.fetchone()

        if courses != None:
            error = "That course already exists"

        if error is None:
            cur.execute("""
             UPDATE courses SET course_number = %s, major = %s, name = %s, description = %s, credits = %s, teacher = %s
             WHERE id = %s;
             """,
             (course_number, g.users['major'], name, description, credits, g.users['id'], course_id))
            db.get_db().commit()
            

            #START OF NEW CODE 
    
            cur.execute("""
            SELECT id FROM courses WHERE id = %s;
            """),
            (id,)
            courses = cur.fetchone()
            course_id = courses[0]

            cur.execute("""SELECT id FROM session
            WHERE name = %s and courses_id = %s;
            """,
            (name, course_id))
            sessions = cur.fetchone()
            session_id = sessions[0]
            cur.close()


            return redirect(url_for('courses.view_course', session_id=session_id, course_id=course_id))
    return render_template('portal/courses/update-course.html')
