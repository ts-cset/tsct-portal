from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session
from . import db
bp = Blueprint("portal", __name__)


@bp.route("/create", methods=['GET', 'POST'])
def create():

    cur = db.get_db().cursor()
    cur.execute("""
        SELECT major_id, name FROM majors""",
                )
    majors = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        teacherId = session['user_id']
        major = request.form['major_id']
        course_name = request.form['new_course']
        course_description = request.form['course_description']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO courses (name, major, description, teacherId)
        VALUES (%s, %s, %s, %s)""",
                    (course_name, major, course_description, teacherId,))

        g.db.commit()
        return redirect(url_for('portal.home'))

    return render_template("create_course.html", majors=majors)
