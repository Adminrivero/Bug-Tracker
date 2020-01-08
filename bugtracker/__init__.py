import os
from flask import Flask, render_template

# create the application factory function.
def create_app(test_config=None):
    # create and configure the flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='devenv',
        DATABASE=os.path.join(app.instance_path, 'bugtracker.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # default route
    @app.route('/hello')
    def hello():
        return "Hello, Welcome to Bug Tracker"
    
    # import 'db' then call function init_app passing the application instance.
    from . import db
    db.init_app(app)

    # import and register blueprint 'auth'
    from . import auth
    app.register_blueprint(auth.bp)

    # import and register blueprint 'dashboard'
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # import and register blueprint 'project'
    from . import project
    app.register_blueprint(project.bp)

    # import and register blueprint 'user'
    from . import user
    app.register_blueprint(user.bp)

    # import and register blueprint 'issue'
    from . import issue
    app.register_blueprint(issue.bp)


    """
    def errorhandler(e):
        # Handle error
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return render_template('errors/page_error.html', code=e.code, name=e.name, desc=e.description), e.code

    # Listen for errors

    for code in default_exceptions:
        current_app.errorhandler(code)(errorhandler)
    """

    return app