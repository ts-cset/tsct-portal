from flask import Blueprint, g, render_template
from . import db
from portal.auth import login_required, student_required

bp = Blueprint("schedule", __name__)


# Page where students can view their schedules
@bp.route("/schedule", methods=('GET', 'POST'))
# I don't think I need the methods here (?)
@login_required
@student_required
def view_schedule():
    """Students can view their schedule here"""

    # This is to test the schedule page
    # cur = db.get_db().cursor()
    # cur.execute('SELECT * FROM users')
    # classes = cur.fetchall()
    # cur.close()

    # Here, I will put what goes into the schedule
    cur = db.get_db().cursor()
    cur.execute("""
        SELECT sessions.session_name,
                sessions.location,
                sessions.room_number,
                sessions.times,
                courses.description,
                users.name,
                rosters.user_id
        FROM sessions
        INNER JOIN courses ON courses.course_num = sessions.course_id
        INNER JOIN users ON courses.teacher_id = users.id
        INNER JOIN rosters ON sessions.id = rosters.session_id
        WHERE courses.major_id = %s""",
        (g.user['major_id'],)
        )
    infos = cur.fetchall()

    cur.close()

    return render_template("layouts/schedule.html", infos=infos)
