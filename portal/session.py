from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

from portal.auth import login_required, admin, validate, validate_text
from portal.teacher import bp

@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
@admin
def sessions():
    if request.method == 'POST':

        items = []
        error = None

        for item in request.form.getlist('id'):
            if validate(item, 'sessions'):
                items.append(int(item))
            else:
                error = 'Something went wrong.'
                break
        if not error:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM sessions
                        WHERE id = ANY(%s)
                    """, (items,))
        else:
            flash(error)

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
    if request.method == "POST":
        course_id = request.form['course_id']

        if validate(course_id, 'courses'):
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
        else:
            flash('Something went wrong.')

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
                    WHERE major = %s AND role = 'student' AND id NOT IN (SELECT student_id FROM roster WHERE session_id = %s)
                """, (course['major'], session['class_session']))

                students = cur.fetchall()

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
    if request.method == 'POST':
        if session.get('class_session'):
            with db.get_db() as con:
                with con.cursor() as cur:
                    for id in request.form:
                        cur.execute("""
                            INSERT INTO roster (student_id, session_id)
                            VALUES (%s, %s)
                        """, (id, session['class_session']))
    if not session.get('edit'):
        return redirect(url_for('teacher.make_session'))
    else:
        return redirect(url_for('teacher.session_edit'))

@bp.route('/sessions/remove', methods=('GET', 'POST'))
@login_required
@admin
def session_remove():
    if request.method == 'POST':
        if session.get('class_session'):
            with db.get_db() as con:
                with con.cursor() as cur:
                    for item in request.form:
                        cur.execute("""
                            DELETE FROM roster
                            WHERE student_id = %s and session_id = %s
                        """, (request.form[item], session['class_session']))
    if not session.get('edit'):
        return redirect(url_for('teacher.make_session'))
    else:
        return redirect(url_for('teacher.session_edit'))

@bp.route('/sessions/submit', methods=('GET', 'POST'))
@login_required
@admin
def session_submit():
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
    if session.get('class_session'):
        if not session.get('edit'):
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        DELETE FROM sessions
                        WHERE id = %s
                    """, (session['class_session'],))
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

    flash(error)

    return redirect(url_for('teacher.home'))

@bp.route('/sessions/edit', methods=('GET', 'POST'))
@login_required
@admin
def session_edit():
    if request.method == "POST":
        session_id = request.form['edit']
        if validate(session_id, 'sessions'):
            session['class_session'] = session_id
            session['edit'] = True
        else:
            flash('Something went wrong.')

    if session.get('edit'):
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM sessions
                    WHERE id = %s
                """, (session['class_session'],))
                session_info = cur.fetchone()

                cur.execute("""
                    SELECT last_name, first_name, id FROM users
                    WHERE role = 'student' AND major IN (SELECT major from courses
                        WHERE id IN (SELECT course_id FROM sessions where id = %s))
                    AND id NOT IN (SELECT student_id FROM roster WHERE session_id = %s)
                """, (session['class_session'], session['class_session']))
                students = cur.fetchall()

                cur.execute("""
                    SELECT u.last_name, u.first_name, u.id FROM roster r JOIN users u
                    ON r.student_id = u.id
                    WHERE r.session_id = %s
                """, (session['class_session'],))

                roster = cur.fetchall()

        return render_template('layouts/teacher/sessions/edit-sessions.html', session_info=session_info, students=students, roster=roster)

    return redirect(url_for('teacher.home'))
