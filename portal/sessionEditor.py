from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash
import functools
from . import courseEditor
from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("sessionEditor", __name__)

@bp.route("/courseSessions/<int:id>/edit/<int:sessions_id>", methods=('GET', 'POST'))
@login_required
@teacher_required
def session_edit(id, sessions_id):
    """Allows teachers to edit a specific session of a
    specific course"""
    course = courseEditor.get_course(id)
    session = get_session(sessions_id)

    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:


                name = request.form['editName']
                times = request.form['editTimes']
                room = request.form['editRoom']
                location = request.form['editLocal']
                error = None

                if error is None:

                    cur.execute("""UPDATE sessions SET
                        name = %s,
                        times = %s,
                        room_number = %s,
                        location = %s
                        WHERE id = %s AND course_id = %s
                        """,
                        (name, times, room, location, sessions_id, id, )
                        )
                    con.commit()

                    return redirect(url_for( 'sessionEditor.session_manage', id=course['course_num']))

                flash(error)


    return render_template("layouts/editSession.html", course=course, session=session)


@bp.route("/createSession/course/<int:id>", methods=('GET','POST'))
@login_required
@teacher_required
def session_create(id):
    """Allows a teacher to create a speficic session in  a
    specific course"""
    course = courseEditor.get_course(id)
    session = get_session(sessions_id)
    students = get_students()



    if request.method == 'POST':


            flash(error)

    return render_template("layouts/createSession.html")


@bp.route("/courseSessions/<int:id>", methods=('GET', 'POST'))
@login_required
@teacher_required
def session_manage(id):
    """The management page of all the sessions in
    a specific course"""

    course = courseEditor.get_course(id)

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM sessions WHERE course_id = %s',
    (id, ))

    sessions = cur.fetchall()

    cur.close()

    return render_template("layouts/sessionManage.html", course=course, sessions=sessions)


def get_session(sessions_id):
    """Gets the session from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
                'SELECT id, times, name, room_number, location, course_id'
                ' FROM sessions WHERE id = %s',
                (sessions_id, )
            )

            session = cur.fetchone()

            if session is None:
                abort(404, "Session id {0} doesn't exist.".format(session_id))

            return session

def get_students():
    """Gets all the students from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
            'SELECT id, name, major_id, email, password, role'
            " FROM users WHERE role = 'student'"
            )

            students = cur.fetchall()

            return students
