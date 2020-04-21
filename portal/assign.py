from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash, abort
import functools

import datetime
from . import session_editor
from . import course_editor
from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("assign", __name__)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/create/assignment/', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_create(sessions_id, course_id):
    """Allows teachers to create new assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    course = course_editor.get_course(course_id)

    if g.user['id'] != course['teacher_id']:
        return redirect(url_for('index'))

    if course['course_num'] != session['course_id']:
        return redirect(url_for('index'))

    if request.method == 'POST':

        name = request.form['name']
        points = request.form['points']
        description = request.form['description']
        due_date = request.form['due_date']
        error = None
        with db.get_db() as con:
            with con.cursor() as cur:

                if not name:
                    error = 'Name is required.'
                try:
                    int(points)
                except ValueError:
                    error = 'Points are numbers only, check your values.'
                try:
                    datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
                except ValueError:
                    error = 'Due Date only allows time data, check your values.'

                if error is None:
                    now = datetime.datetime.utcnow()
                    cur.execute("""INSERT INTO assignments (sessions_id, assign_name, description, points, due_time)
                        VALUES (%s, %s, %s, %s, %s)
                    """,
                    (sessions_id, name, description, points, due_date, )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage", sessions_id=session['id'], course_id=session['course_id'] ))

                flash(error)

    return render_template('layouts/assigns/assign_create.html', session=session)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/assignments/', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_manage(course_id, sessions_id):
    """Allows teachers to see current assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    course = course_editor.get_course(course_id)

    if g.user['id'] != course['teacher_id']:
        return redirect(url_for('index'))

    if course['course_num'] != session['course_id']:
        return redirect(url_for('index'))

    cur=db.get_db().cursor()
    cur.execute(
        'SELECT * FROM assignments WHERE sessions_id = %s',
        (sessions_id, )
    )

    assignments = cur.fetchall()

    cur.close()

    return render_template("layouts/assigns/assign_manage.html", assignments=assignments, session=session)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/Edit/assignment/<int:assign_id>/', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_edit(course_id, assign_id, sessions_id):
    """Allows teachers to edit current assignments for a
    specific session"""

    course = course_editor.get_course(course_id)
    session = session_editor.get_session(sessions_id)
    assignment = get_assignment(assign_id)

    if g.user['id'] != course['teacher_id']:
        return redirect(url_for('index'))

    if course['course_num'] != session['course_id']:
        return redirect(url_for('index'))

    if session['id'] != assignment['sessions_id']:
        return redirect(url_for('index'))

    if request.method == 'POST':

        name = request.form['edit_name']
        points = request.form['edit_points']
        description = request.form['edit_desc']
        due_date = request.form['edit_date']
        print(due_date)
        error = None

        with db.get_db() as con:
            with con.cursor() as cur:
                if not name:
                    error = 'Name is required.'
                try:
                    int(points)
                except ValueError:
                    error = 'Points are numbers only, check your values.'
                try:
                    datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
                except ValueError:
                    error = 'Due Date only allows time data, check your values.'

                if error is None:

                    now = datetime.datetime.utcnow()
                    cur.execute("""UPDATE assignments SET
                    assign_name = %s,
                    description = %s,
                    points = %s,
                    due_time = %s
                    WHERE id = %s AND sessions_id = %s
                    """,
                    (name, description, points, due_date, assign_id, sessions_id, )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage",course_id=session['course_id'], sessions_id=session['id']))

                flash(error)

    return render_template('layouts/assigns/assign_edit.html', session=session, assignment= assignment)

def get_assignment(assign_id):
    """Gets the assiment from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute(
                'SELECT id, assign_name, description, points, sessions_id, due_time'
                ' FROM assignments WHERE id = %s',
                (assign_id, )
            )
            assign = cur.fetchone()

            if assign is None:
                abort(404, "Assign id {0} doesn't exist.".format(assign_id))

            return assign
