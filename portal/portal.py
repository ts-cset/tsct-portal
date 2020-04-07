import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db

bp = Blueprint('portal', __name__, url_prefix='/portal')

@bp.route('/userpage')
def userpage():
    return render_template('account/home.html')
