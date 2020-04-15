from flask import render_template, Blueprint, session, g, flash, request

from . import db

bp = Blueprint("roster", __name__)


@bp.route('/roster', methods=('GET', 'POST'))
def display_roster():

    #Test variables
    course = { 'name': 'CSET 180' }
    session = { 'name': 'A' }
    students = [
        {
            'name': 'John Smith',
            'email': 'smithj@stevenscollege.edu'
        },
        {
            'name': 'Example McTest',
            'email': 'example@stevenscollege.edu'
        }
    ]

    if request.method == 'POST':

        email = request.form['email']
        already_enrolled = False
        error = None

        with db.get_db() as con:
            with con.cursor() as cur:

                # Find the student in the users table
                cur.execute("""SELECT name, email, role FROM users
                    WHERE email = %s""", (email,))

                user = cur.fetchone()

                # Check if the student is already in the current session

        # If there is no student with the entered email create an error message
        if user == None:

            error = 'No student found'

        # If the selected user is not a student, create an error message
        if user['role'] != 'student':

            error = f'{user['name']} is not a student'

        # If the student is already in the session create an error message
        if already_enrolled:

            error = f'{user['name']} is already enrolled in this session.'

        if error == None:

            #Insert user into the roster
            pass

        else:

            flash(error)


    return render_template('roster.html', course=course, session=session, students=students)
