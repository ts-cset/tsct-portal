from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required,teacher_required

bp = Blueprint("roster", __name__)

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
        message = ""
        #cur=con.cursor()
        #cur.execute(
        #"""SELECT name FROM users """
        #)
        #names = cur.fetchall()
        #cur.close()

        #namesb = []is not
        #for name in range(len(names)):
        #    namesb.append(name)
        studentname = request.form['sname']
        cur = con.cursor()
        cur.execute('SELECT name, id FROM users WHERE name = %s',(studentname,))
        bname = cur.fetchone()
        if bname is not None:
            bid = bname['id']
            cur.execute('SELECT student_id, session_id FROM roster WHERE student_id = %s AND session_id = %s',
            (bid, '1'))
            matching = cur.fetchall()
            if matching is None:
                message = "{} added".format(studentname)
                cur= con.cursor()
                newid = bname['id']
                print(newid)
                cur.execute(
                """INSERT INTO roster (student_id , session_id)
                VALUES (%s, %s)""",
                (newid,'1'))
                con.commit()
                cur.close()
            else:
                message ="{} is already in the roster".format(studentname)
        else:
            message = "Error: student not found"
        cur.close()
        con.close()
    return render_template("layouts/sessions/roster.html", students=students, message=message)
