from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('gradebook', __name__, url_prefix='/gradebook')

@bp.route('/gradebook')
@login_required
def gradebook():
    cur = db.get_db().cursor()
    cur.execute("""SELECT * FROM courses""")
    courses = cur.fetchall()
    cur.execute("""SELECT courses.id AS c_id, session.* FROM session
                   JOIN courses ON courses.id = session.courses_id""")
    sessions = cur.fetchall()
    cur.execute("""SELECT session.id AS s_id, assignments.* FROM assignments
                   JOIN session ON session.id = assignments.session_id""")
    assignments = cur.fetchall()
    cur.execute("""SELECT session.id AS s_id, roster.* FROM roster
                   JOIN session ON session.id = roster.session_id""")
    rosters = cur.fetchall()
    if g.users['role'] == 'teacher':
        cur.execute("""SELECT grades.letter, submissions.* FROM submissions
                       JOIN grades ON submissions.grades_id = grades.id""")
        submissions = cur.fetchall()
    else:
        cur.execute("""SELECT grades.letter, submissions.* FROM submissions
                       JOIN grades ON submissions.grades_id = grades.id
                       WHERE users_id = %s;""",
                       (g.users['id'],))
        submissions = cur.fetchall()
    cur.close()
    return render_template('portal/gradebook/view-gradebook.html', courses=courses, sessions=sessions, assignments=assignments, rosters=rosters, submissions=submissions)

@bp.route('/<path:subpath>/')
@login_required
def gradebook_error(subpath=None):
    error = "404 Not found"
    return render_template('error.html', error=error)
