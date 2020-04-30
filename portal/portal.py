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
