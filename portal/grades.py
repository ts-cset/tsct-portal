from flask import (
    Blueprint, g, render_template, redirect, url_for, session, request, flash
)

from portal.db import get_db

bp = Blueprint('grades', __name__)

@bp.route('/grades', methods=('GET', 'POST'))
def grades():
    pass
