from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('sessions', __name__, url_prefix='/portal/sessions')

@bp.route('/<course_id>/view-session/<session_id>', methods=('GET', 'POST'))
@login_required
def view_session(course_id, session_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses
                   WHERE id = %s;""",
                   (course_id,))
    courses = cur.fetchall()
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM session
                   WHERE id = %s;""",
                   (session_id,))
    sessions = cur.fetchall()

    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM assignments
                   WHERE session_id = %s;""",
                   (session_id,))
    assignments = cur.fetchall()

    cur.execute("""SELECT * FROM roster
                   WHERE session_id = %s;""",
                   (session_id,))
    rosters = cur.fetchall()
    cur.close()
    return render_template('portal/courses/sessions/view-session.html', courses=courses, sessions=sessions, rosters=rosters, assignments=assignments)

@bp.route('/<course_id>/create-session', methods=('GET', 'POST'))
@login_required
@teacher_required
def create_session(course_id):
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM users
                   WHERE role = 'student'""")
    students = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        name = request.form['name']
        times = request.form['times']
        students = request.form.getlist('students')
        error = None
        cur = db.get_db().cursor()
        cur.execute("""
        SELECT * FROM session
        WHERE name = %s and courses_id = %s;
        """,
        (name, course_id))
        session = cur.fetchone()

        if session != None:
            error = "That session already exists"
            return render_template('error.html', error=error)

        if error is None:
            try:
                cur.execute("""INSERT INTO session (courses_id, times, name)
                VALUES (%s, %s, %s);
                 """,
                 (course_id, times, name))
                db.get_db().commit()
            except:
                error = "There was a problem creating that session"
                return render_template('error.html', error=error)
            else:
                cur.execute("""SELECT id FROM session
                               WHERE courses_id = %s and name = %s and times = %s""",
                               (course_id, name, times))
                session = cur.fetchone()

            for student in students:
                cur.execute("""INSERT INTO roster (users_id, session_id)
                VALUES (%s, %s);
                 """,
                 (student, session[0]))
                db.get_db().commit()

#new code for the routes and trying to get back to the view-sessions page

#for this i need the course_id the session_id, roster_id, and assignment_id to get it to work

#assingment_id attmept
            cur.execute("""SELECT id FROM session
            WHERE name = %s and courses_id = %s;
            """,
            (name, course_id))
            sessions = cur.fetchone()
            session_id = sessions[0]
            
            cur.execute("""SELECT id FROM assignments WHERE name = %s 
                    and session_id = %s;""",
                    (name, session_id))
            assignment_id = cur.fetchone()
            

            cur.execute("""SELECT id FROM roster
                   WHERE session_id = %s;""",
                   (session_id,))
            rosters = cur.fetchone()
            roster_id = rosters[0]
        
            #end of new code 
        
        
            return redirect(url_for('sessions.view_session', session_id=session_id, course_id=course_id, assignment_id=assignment_id, roster_id=roster_id))
        else:
            return redirect(url_for('sessions.create_session', course_id=course_id))
    return render_template('portal/courses/sessions/create-session.html', students=students)

@bp.route('/<path:subpath>/')
@login_required
def session_error(subpath=None):
    error = "404 Not found"
    return render_template('error.html', error=error)
