from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role

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
        con = db.get_db()
        cur = con.cursor()
        cur.execute('SELECT name, id FROM users WHERE name = %s',(studentname,))
        bname = cur.fetchone()
        con.commit()
        cur.close()
        if bname is not None:
            con = db.get_db()
            cur= con.cursor()
            newid = bname['id']
            print(newid)
            cur.execute(
            """INSERT INTO roster (student_id , session_id)
            VALUES (%s, %s)""",
            (newid,'1'))
            con.commit()
            cur.close()
    return render_template("layouts/sessions/roster.html", students=students, bname=bname)
