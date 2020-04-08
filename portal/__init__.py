import os

from flask import Flask, render_template, Blueprint, request, redirect, url_for, g, flash, session

from . import db

def create_app(test_config=None):
    """Factory to configure and return a Flask application.

    Keyword arguments:
    test_config -- dictionary to configure the app for tests (default None)
    """

    # Create the Flask application object using this module's name
    app = Flask(__name__, instance_relative_config=True)

    # Configure App
    # -------------
    # Default configuration, can be overwritten by specific environment
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_URL="postgresql://portal_user@localhost/portal",
        DB_SSLMODE="allow",
    )

    if test_config is None:
        # App configuration for dev or prod if `config.py` exists
        app.config.from_pyfile("config.py", silent=True)

        # Check for environment variables on Heroku
        prod_db_url = os.environ.get("DATABASE_URL", None)
        if prod_db_url is not None:
            app.config.from_mapping(
                DB_URL=prod_db_url,
                DB_SSLMODE="require"
            )
    else:
        # App configuration specifically for tests
        app.config.from_mapping(test_config)

    # Setup Database
    # --------------
    from . import db
    db.init_app(app)

    # Register Routes
    # ---------------
    from . import auth, student
    app.register_blueprint(auth.bp)
    app.register_blueprint(student.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/ClassCreation', methods=('GET', 'POST'))
    def classCreation():
        if request.method == "POST":
            className = request.form['Class-Name']
            classSubject = request.form['Class-Major']
            classDescription = request.form['description']
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses(course_code, course_name, major, description) VALUES(%s, %s, %s, %s)",
                    (50, className, classSubject, classDescription)
                    )
            cur = db.get_db().cursor()
            cur.execute("SELECT * FROM courses")
            courses = cur.fetchall()
            cur.close()
            return render_template("class.html", courses=courses)
        return render_template("CourseCreation.html")

    # Return application object to be used by a WSGI server, like gunicorn
    return app
