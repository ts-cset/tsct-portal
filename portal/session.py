from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role

bp = Blueprint("session", __name__)

#Route for viewing sessions
@bp.route("/<int:id>/sessions", methods=['GET', 'POST'])
@login_required
def view_sessions(id):
    """Single page view of course"""
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""SELECT * FROM sessions where course = %s""",
                (id,))
    # cur.execute("""SELECT sessions.course, sessions.days, sessions.class_time, courses.teacherid, users.name AS teacher_name FROM sessions INNER JOIN users ON courses.teacherid = users.id WHERE courses.course_id = %s""",
    #             (id,))
    sessions = cur.fetchall()
    cur.close()
    con.close()
    return render_template("layouts/sessions/view_sessions.html", sessions=sessions)

#Route to roster
@bp.route("/roster", methods= ('GET', 'POST'))
def roster():
    bname = ''
    con = db.get_db()
    cur = con.cursor()
    cur.execute(
    """SELECT roster.student_id, roster.session_id, users.id, users.name FROM roster JOIN users ON roster.student_id = users.id WHERE session_id = 1 ORDER BY users.name DESC""")
    students = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        #cur=con.cursor()
        #cur.execute(
        #"""SELECT name FROM users """
        #)
        #names = cur.fetchall()
        #cur.close()

        #namesb = []
        #for name in range(len(names)):
        #    namesb.append(name)

        studentname = request.form['sname']
        con = db.get_db()
        cur = con.cursor()
        cur.execute('SELECT name, id FROM users WHERE name = %s',(studentname,))
        bname = cur.fetchone()
        bname['name']
        con.commit()
        cur.close()
        if bname['name'] != None:
            con = db.get_db()
            cur= con.cursor()
            newid = bname['id']
            print(newid)
            cur.execute(
            """INSERT INTO roster (student_id , session_id)
            VALUES (s%, 1)""",
            (newid))
            con.commit()
            cur.close()
    return render_template("layouts/sessions/roster.html", students=students, bname=bname)
