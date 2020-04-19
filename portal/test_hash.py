from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools
from . import db
from werkzeug.security import check_password_hash, generate_password_hash



PASSWORD = password
test = generate_password_hash(PASSWORD)

print(generate_password_hash(PASSWORD))
