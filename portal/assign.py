from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash, abort
import functools

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("assign", __name__)

@bp.route('/assignCreate' methods = ('GET', 'POST'))
@login_required
@teacher_required

def assign_create():
    """Allows teachers to create new assignments for a
    specific session"""

    pass

@bp.route('/assignManage' methods = ('GET', 'POST'))
@login_required
@teacher_required

def assign_manage():
    """Allows teachers to see current assignments for a
    specific session"""

    pass

@bp.route('/assignVeiw' methods = ('GET', 'POST'))
@login_required
@teacher_required

def assign_veiw():
    """Allows teachers to see current assignments details for a
    specific assignment in a specific session"""

    pass

@bp.route('/assignEdit' methods = ('GET', 'POST'))
@login_required
@teacher_required


def assign_edit():
    """Allows teachers to edit current assignments for a
    specific session"""

    pass
