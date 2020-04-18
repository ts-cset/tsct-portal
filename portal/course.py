from portal.auth import login_required, teacher_required

from . import db

from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

bp = Blueprint("course", __name__)


# Function used to get a specific course
def get_course(id, check_teacher=True):

    user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute("""SELECT course_id, name, description, teacherid FROM courses WHERE teacherid = %s AND course_id = %s""",
                (user_id, id,))
    course = cur.fetchone()
    cur.close()

    if course is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_teacher and course['teacherid'] != g.user['id']:
        abort(403)

    return course


# route to edit the course description
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@teacher_required
@login_required
def edit(id):
    """Edits the description of the courses"""
    course = get_course(id)

    if request.method == 'POST':

        teacherid = session['user_id']
        course_name = request.form['new_course']
        course_description = request.form['course_description']

        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE courses SET name = %s, description = %s'
            ' WHERE course_id = %s ',
            (course_name, course_description, id)
        )
        con.commit()
        db.close_db()

        return redirect(url_for('course.view', id=course['course_id']))

    return render_template("layouts/courses/edit.html", course=course)


# Route to view the course, and information about it
@bp.route('/<int:id>/view', methods=('GET', 'POST'))
@teacher_required
@login_required
def view(id):
    """Single page view of a course"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT courses.course_id, courses.name, courses.major, courses.description, courses.teacherid, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id WHERE courses.course_id = %s""",
                (id,))
    course = cur.fetchone()
    cur.close()

    return render_template("layouts/courses/view_course.html", course=course)


# Route to delete a course

@bp.route("/<int:id>/delete", methods=["POST", ])
@teacher_required
@login_required
def delete(id):
    """Delete unwanted courses"""
    course = get_course(id)
    cur = db.get_db().cursor()
    cur.execute(
        'DELETE FROM courses WHERE course_id= %s', (id,)
    )
    con.commit()
    return redirect(url_for('main.home'))

# Route to create a course
@bp.route("/create", methods=['GET', 'POST'])
@teacher_required
@login_required
def create():
    cur = db.get_db().cursor()
    cur.execute("""
        SELECT major_id, name FROM majors""",
                )
    majors = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        teacherId = session['user_id']
        major = request.form['majors']
        course_name = request.form['new_course']
        course_description = request.form['course_description']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO courses (name, major, description, teacherId)
        VALUES (%s, %s, %s, %s)""",
                    (course_name, major, course_description, teacherId,))

        con.commit()
        close_db()
        return redirect(url_for('main.home'))

    return render_template("layouts/courses/create_courses.html", majors=majors)
