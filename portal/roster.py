from flask import render_template, Blueprint, session, g, flash

from . import db

bp = Blueprint("roster", __name__)


@bp.route('/roster', methods=('GET', 'POST'))
def display_roster():

    #Test variables
    course = { 'name': 'CSET 180'}
    session = { 'name': 'A'}
    students = [
        {
            'name': 'John Smith',
            'email': 'smithj@stevenscollege.edu'
        },
        {
            'name': 'Example McTest',
            'email': 'student@stevenscollege.edu'
        }
    ]


    return render_template('roster.html', course=course, session=session, students=students)
