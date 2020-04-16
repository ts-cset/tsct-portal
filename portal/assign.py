from flask import redirect, g, url_for, render_template, session, request, Blueprint, flash, abort
import functools

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("assign", __name__)
