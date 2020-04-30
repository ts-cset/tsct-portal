import os

from flask import Flask, render_template


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

    # Login Users
    # ---------------
    from . import auth
    app.register_blueprint(auth.bp)

    # Portal
    # ---------------
    from . import portal
    app.register_blueprint(portal.bp)

    # Courses
    # ---------------
    from . import courses
    app.register_blueprint(courses.bp)

    # Sessions
    # ---------------
    from . import sessions
    app.register_blueprint(sessions.bp)

    # Assignments
    #----------------
    from . import assignments
    app.register_blueprint(assignments.bp)

    # Gradebook
    #----------------
    from . import gradebook
    app.register_blueprint(gradebook.bp)

    # Home Page
    # ---------------
    @app.route('/')
    def index():
        return render_template('index.html')

    # Error Page
    # ---------------
    @app.route('/<path:subpath>/')
    def error(subpath=None):
        error = "404 Not found"
        return render_template('error.html', error=error)

    # Return application object to be used by a WSGI server, like gunicorn
    return app
