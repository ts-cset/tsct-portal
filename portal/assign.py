from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash, abort
import functools

from . import session_editor
from . import course_editor
from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("assign", __name__)

@bp.route('/assignCreate/<int:id>/<int:sessions_id>', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_create(id, sessions_id):
    """Allows teachers to create new assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    course = course_editor.get_course(id)

    if request.method == 'POST':

        name = request.form['name']
        points = request.form['points']
        description = request.form['description']
        error = None

        with db.get_db() as con:
            with con.cursor() as cur:

                if not name:
                    error = 'Name is required.'
                if not points:
                    error = 'Points is required.'
                if not description:
                    error = 'Description is required.'

                if error is None:

                    cur.execute("""INSERT INTO assignments (course_id, sessions_id, assign_name, description, points)
                        VALUES (%s, %s, %s, %s, %s )
                    """,
                    (id, sessions_id, name, description, points, )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage", sessions_id=session['id'], id=course['course_num']))

                flash(error)

    return render_template('layouts/assigns/assign_create.html', course=course, session=session)

@bp.route('/assignManage/<int:id>/<int:sessions_id>', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_manage(id, sessions_id):
    """Allows teachers to see current assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    course = course_editor.get_course(id)

    cur=db.get_db().cursor()
    cur.execute(
        'SELECT * FROM assignments WHERE sessions_id = %s',
        (sessions_id, )
    )

    assignments = cur.fetchall()

    cur.close()

    return render_template("layouts/assigns/assign_manage.html", assignments=assignments, session=session, course=course)

@bp.route('/assignVeiw', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_veiw():
    """Allows teachers to see current assignments details for a
    specific assignment in a specific session"""

    pass

@bp.route('/assignEdit', methods=('GET', 'POST'))
@login_required
@teacher_required


def assign_edit():
    """Allows teachers to edit current assignments for a
    specific session"""

    pass


def get_assignment(assign_id):
    """Gets the assiment from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute(
                'SELECT id, name, description, points, session_id'
                ' FROM assignments WHERE id = %s',
                (assign_id, )
            )
            assign = cur.fetchone()

            if assign is None:
                abort(404, "Assign id {0} doesn't exist.".format(assign_id))

            return assign
