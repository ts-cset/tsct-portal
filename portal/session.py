from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin, validate, validate_text
from portal.teacher import bp

@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
@admin
def sessions():
    """Display a list of sessions that the logged-in user owns and can delete"""
    if request.method == 'POST':

        items = []
        error = None

        # Collect all the checked form items and validate ownership
        for item in request.form.getlist('id'):
            if validate(item, 'sessions'):
                items.append(int(item))
            else:
                # If validation fails, set an error and stop the loop
                error = 'Something went wrong.'
                break

        # If all validation succeeds, delete selected sessions from the DB
        if not error:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM sessions
                        WHERE id = ANY(%s)
                    """, (items,))
        else:
            # If validation fails, prepare an error to be shown to the user
            flash(error)

    # Grab all sessions that the teacher owns from the DB along with associated
    # course information
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT s.id, s.session_name, c.course_code, c.course_name, c.major
                FROM sessions s JOIN courses c
                ON s.course_id = c.id
                WHERE c.teacher_id = %s
                ORDER BY c.major, s.session_name
            """, (g.user['id'],))
            sessions = cur.fetchall()
    return render_template('layouts/teacher/sessions/sessions.html', sessions=sessions)


@bp.route('/sessions/create', methods=('GET', 'POST'))
@login_required
@admin
def make_session():
    """Begin creation of a course session"""
    if request.method == "POST":
        # Obtain id of parent course for session
        course_id = request.form['course_id']

        # Validate that the teacher owns the parent course
        if validate(course_id, 'courses'):
            # Add the course ID to the global HTTP session variable
            session['course_id'] = course_id
            # Add an incomplete session entry to the database to enable roster creation;
            # then, select that new session.
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        INSERT INTO sessions (course_id)
                        VALUES (%s);
                        SELECT * FROM sessions
                        WHERE course_id = %s
                        ORDER BY id DESC
                    """, (course_id, course_id))

                    # Get the new session ID and add it to the global session
                    # variable to create a session-creation state
                    session_id = cur.fetchone().get('id')
                    session['class_session'] = session_id
        else:
            # If validation fails, prepare an error to be shown to the user
            flash('Something went wrong.')

    # Check that session creation is currently underway
    if session.get('class_session'):
        # Get course information, valid student users, and students currently on
        # the session roster from the database
        with db.get_db() as con:
            with con.cursor() as cur:
                # Grab the parent course information from the database
                cur.execute("""
                    SELECT * FROM courses
                    WHERE id = %s
                """, (session['course_id'],))
                course = cur.fetchone()

                # If the parent course major is general education, select all students
                # not already on the roster; otherwise, select all students with the
                # same major as the parent course who are not already on the roster
                if course['major'] == 'GEN':
                    cur.execute("""
                        SELECT * FROM users
                        WHERE role = 'student' and id NOT IN (SELECT student_id from ROSTER WHERE session_id = %s)
                    """, (session['class_session'],))
                else:
                    cur.execute("""
                        SELECT * FROM users
                        WHERE major = %s AND role = 'student' AND id NOT IN (SELECT student_id FROM roster WHERE session_id = %s)
                    """, (course['major'], session['class_session']))

                students = cur.fetchall()

                # Grab the current roster for the session
                cur.execute("""
                    SELECT u.last_name, u.first_name, u.id FROM roster r JOIN users u
                    ON r.student_id = u.id
                    WHERE r.session_id = %s
                """, (session['class_session'],))

                roster = cur.fetchall()

        return render_template('layouts/teacher/sessions/create-sessions.html', students=students, roster=roster)
    else:
        return redirect(url_for('teacher.courses'))


@bp.route('/sessions/add', methods=('GET', 'POST'))
@login_required
@admin
def session_add():
    """Add students to a session roster during creation or editing"""
    if request.method == 'POST':
        if session.get('class_session'):

            ids = []
            error = None

            # Confirm that every checked box id is for a valid student
            for id in request.form.getlist('id'):
                if validate(id, 'users'):
                    ids.append(int(id))
                else:
                    # If any id is not valid, set an error and stop the loop
                    error = "Something went wrong."
                    break

            # If validation completes successfully, add all of the students to
            # to the roster
            if not error:
                with db.get_db() as con:
                    with con.cursor() as cur:
                        for id in ids:
                            cur.execute("""
                                INSERT INTO roster (student_id, session_id)
                                VALUES (%s, %s)
                            """, (id, session['class_session']))
            else:
                # If validation fails, prepare an error to be shown to the user
                flash(error)

    if not session.get('edit'):
        return redirect(url_for('teacher.make_session'))
    else:
        return redirect(url_for('teacher.session_edit'))

@bp.route('/sessions/remove', methods=('GET', 'POST'))
@login_required
@admin
def session_remove():
    """Remove students from a session roster during creation or editing"""
    if request.method == 'POST':
        if session.get('class_session'):

            ids = []
            error = None

            # Confirm that each checked box is a valid student user
            for id in request.form.getlist('id'):
                if validate(id, 'users'):
                    ids.append(int(id))
                else:
                    # If any id fails validation, prepare an error and stop looping
                    error = "Something went wrong."
                    break

            # If validation passes, delete students from the roster in the DB
            if not error:
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            DELETE FROM roster
                            WHERE student_id = ANY(%s) AND session_id = %s
                        """, (ids, session['class_session']))
            else:
                # If validation fails, prepare an error to be shown to the user
                flash(error)

    if not session.get('edit'):
        return redirect(url_for('teacher.make_session'))
    else:
        return redirect(url_for('teacher.session_edit'))

@bp.route('/sessions/submit', methods=('GET', 'POST'))
@login_required
@admin
def session_submit():
    """Finalize session creation with extra data and end session creation state"""
    if request.method == 'POST':
        if session.get('class_session'):
            session_name = request.form['session_name']
            meeting_days = request.form['meeting_days']
            meeting_place = request.form['meeting_place']
            meeting_time = request.form['meeting_time']
            # validate length of text input before proceeding
            if (
                validate_text(session_name, 1) and
                validate_text(meeting_days, 6) and
                validate_text(meeting_place, 10) and
                validate_text(meeting_time, 11)
                ):
                # if all validation passes, open a DB connection
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            UPDATE sessions
                            SET session_name = %s,
                                meeting_days = %s,
                                meeting_place = %s,
                                meeting_time = %s
                            WHERE id = %s
                        """, (session_name, meeting_days, meeting_place, meeting_time, session['class_session']))

                return redirect(url_for('teacher.sessions'))
            # if any validation fails, store an error and continue to redirect
            else:
                flash('Something went wrong. Editing canceled.')

            # Remove keys related to session creation state from the global session
            session.pop('class_session', None)
            session.pop('course_id', None)
            session.pop('edit', None)

    if not session.get('edit'):
        return redirect(url_for('teacher.make_session'))
    else:
        return redirect(url_for('teacher.session_edit'))

@bp.route('/sessions/cancel')
@login_required
@admin
def session_cancel():
    """Cancel session creation and end session creation state"""
    if session.get('class_session'):
        # If an edit is not in progress, canceling means deleting the temporary
        # session from the database
        if not session.get('edit'):
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM sessions
                        WHERE id = %s
                    """, (session['class_session'],))
            # In either case, session creation keys need to be removed from the
            # global session variable
            session.pop('class_session', None)
            session.pop('course_id', None)
            error = "Session creation canceled"
        else:
            session.pop('class_session', None)
            session.pop('course_id', None)
            session.pop('edit', None)
            error = "Session edit canceled"
    else:
        error = "Not able to cancel session"

    # Store a message to be shown to the user to indicate the result of the cancellation
    flash(error)

    return redirect(url_for('teacher.home'))

@bp.route('/sessions/edit', methods=('GET', 'POST'))
@login_required
@admin
def session_edit():
    """Set global session edit state and show the session edit form"""
    if request.method == "POST":
        # Get target session id from form
        session_id = request.form['edit']
        # Confirm that the logged-in teacher owns the session
        if validate(session_id, 'sessions'):
            # Set global session values to create session editing state
            session['class_session'] = session_id
            session['edit'] = True
        else:
            # If validation fails, prepare an error to be shown to the user
            flash('Something went wrong.')

    # If the session is in the edit state, fetch info from the DB to be shown
    # on the editing form
    if session.get('edit'):
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM sessions s JOIN courses c
                    ON s.course_id = c.id
                    WHERE s.id = %s
                """, (session['class_session'],))
                session_info = cur.fetchone()

                # As with creation, all students should be available to be added to
                # the roster for Gen. Ed. classes
                if session_info['course_id'] == 'GEN':
                    cur.execute("""
                        SELECT last_name, first_name, id FROM users
                        WHERE role = 'student'
                        AND id NOT IN (SELECT student_id FROM roster WHERE session_id = %s)
                    """, (session['class_session'],))
                else:
                    cur.execute("""
                        SELECT last_name, first_name, id FROM users
                        WHERE role = 'student' AND major = %s
                        AND id NOT IN (SELECT student_id FROM roster WHERE session_id = %s)
                    """, (session_info['major'], session['class_session']))

                students = cur.fetchall()

                cur.execute("""
                    SELECT u.last_name, u.first_name, u.id FROM roster r JOIN users u
                    ON r.student_id = u.id
                    WHERE r.session_id = %s
                """, (session['class_session'],))

                roster = cur.fetchall()

        return render_template('layouts/teacher/sessions/edit-sessions.html', session_info=session_info, students=students, roster=roster)

    return redirect(url_for('teacher.home'))
