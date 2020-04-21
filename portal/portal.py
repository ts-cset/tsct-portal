from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from portal.auth import (login_required, teacher_required)
from . import db

bp = Blueprint('portal', __name__, url_prefix='/portal')

@bp.route('/userpage')
@login_required
def userpage():
    return render_template('account/home.html')

@bp.route('/<route>')
@login_required
def error(route=None):
    error = "404 Not found"
    return render_template('error.html', error=error)
