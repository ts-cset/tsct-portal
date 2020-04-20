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

    course = course_editor.get_course(course_id)

    if g.user['id'] != course['teacher_id']:
        return redirect(url_for('index'))

    session = session_editor.get_session(sessions_id)
    # course = course_editor.get_course(id)

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
                if not points:
                    error = 'Points are required.'
                if not due_date:
                    error = 'Due Date is required.'

                if error is None:
                    print(due_date)
                    now = datetime.datetime.utcnow()

                    cur.execute("""INSERT INTO assignments (sessions_id, assign_name, description, points, due_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """,
                    (sessions_id, name, description, points, due_date )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage", sessions_id=session['id'], course_id=course['course_num'] ))

                flash(error)

    return render_template('layouts/assigns/assign_create.html', session=session, course=course)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/assignments/', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_manage(course_id, sessions_id):
    """Allows teachers to see current assignments for a
    specific session"""

    course = course_editor.get_course(course_id)
    session = session_editor.get_session(sessions_id)
    if g.user['id'] != course['teacher_id']:
        print('hello?')
        return redirect(url_for('index'))
    #course = course_editor.get_course(id)

    cur=db.get_db().cursor()
    cur.execute(
        'SELECT * FROM assignments WHERE sessions_id = %s',
        (sessions_id, )
    )

    assignments = cur.fetchall()

    cur.close()

    return render_template("layouts/assigns/assign_manage.html", assignments=assignments, session=session, course=course)

@bp.route('/course/<int:course_id>/session/<int:sessions_id>/Edit/assignment/<int:assign_id>/', methods=('GET', 'POST'))
@login_required
@teacher_required

def assign_edit(course_id, assign_id, sessions_id):
    """Allows teachers to edit current assignments for a
    specific session"""

    session = session_editor.get_session(sessions_id)
    assignment = get_assignment(assign_id)
    course = course_editor.get_course(course_id)

    if g.user['id'] != course['teacher_id']:
        print('hello')
        return redirect(url_for('index'))

    if request.method == 'POST':

        name = request.form['edit_name']
        points = request.form['edit_points']
        description = request.form['edit_desc']
        due_date = request.form['edit_date']
        error = None

        with db.get_db() as con:
            with con.cursor() as cur:
                print(due_date)
                if not name:
                    error = 'Name is required.'
                if not points:
                    error = 'Points are required.'
                if not due_date:
                    error = 'Due Date is required.'

                if error is None:

                    now = datetime.datetime.utcnow()
                    cur.execute("""UPDATE assignments SET
                    assign_name = %s,
                    description = %s,
                    points = %s,
                    due_date = %s
                    WHERE id = %s AND sessions_id = %s
                    """,
                    (name, description, points, due_date, assign_id, sessions_id, )
                    )
                    con.commit()

                    return redirect(url_for("assign.assign_manage",course_id=course['course_num'], sessions_id=session['id']))

                flash(error)

    return render_template('layouts/assigns/assign_edit.html', session=session, assignment= assignment, course=course)

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

def get_course_2(course_id):
    """Gets the course from the database"""
    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute(
                'SELECT course_num, credits, description, course_title, teacher_id'
                ' FROM courses WHERE course_num = %s',
                (course_id,))

            course = cur.fetchone()

            if course is None:
                abort(404, "Course id {0} doesn't exist.".format(id))

            return course
