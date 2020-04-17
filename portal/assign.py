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
    # course = course_editor.get_course(id)

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
                    error = 'Points are required.'

                if error is None:

                    cur.execute("""INSERT INTO assignments (sessions_id, assign_name, description, points)
                        VALUES (%s, %s, %s, %s)
                    """,
                    (sessions_id, name, description, points, )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage",id=session['course_id'], sessions_id=session['id']))

                flash(error)

    return render_template('layouts/assigns/assign_create.html', session=session)

@bp.route('/assignManage/<int:id>/<int:sessions_id>', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_manage(id, sessions_id):
    """Allows teachers to see current assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    #course = course_editor.get_course(id)

    cur=db.get_db().cursor()
    cur.execute(
        'SELECT * FROM assignments WHERE sessions_id = %s',
        (sessions_id, )
    )

    assignments = cur.fetchall()

    cur.close()

    return render_template("layouts/assigns/assign_manage.html", assignments=assignments, session=session)

@bp.route('/assignVeiw', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_veiw():
    """Allows teachers to see current assignments details for a
    specific assignment in a specific session"""

    pass

@bp.route('/assignEdit/<int:sessions_id>/<int:assign_id>', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_edit(assign_id, sessions_id):
    """Allows teachers to edit current assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    assignment = get_assignment(assign_id)

    if request.method == 'POST':

        name = request.form['edit_name']
        points = request.form['edit_points']
        description = request.form['edit_desc']
        error = None

        with db.get_db() as con:
            with con.cursor() as cur:

                if not name:
                    error = 'Name is required.'
                if not points:
                    error = 'Points are required.'

                if error is None:

                    cur.execute("""UPDATE assignments SET
                    assign_name = %s,
                    description = %s,
                    points = %s
                    WHERE id = %s AND sessions_id = %s
                    """,
                    (name, description, points, assign_id, sessions_id,)
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage",id=session['course_id'], sessions_id=session['id']))

                flash(error)

    return render_template('layouts/assigns/assign_edit.html', session=session, assignment= assignment)

def get_assignment(assign_id):
    """Gets the assiment from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute(
                'SELECT id, assign_name, description, points, sessions_id'
                ' FROM assignments WHERE id = %s',
                (assign_id, )
            )
            assign = cur.fetchone()

            if assign is None:
                abort(404, "Assign id {0} doesn't exist.".format(assign_id))

            return assign
