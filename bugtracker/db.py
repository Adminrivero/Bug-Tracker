import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# gat an instance of the database connection
def get_db():
    if 'db' not in g:
        # establish a connection to the database file.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tell the connection to return rows that behave like dicts.
        g.db.row_factory = sqlite3.Row

    return g.db

# close database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# execute external script to create db objects
def init_db():
    db = get_db()

    # loads database script from bugtracker.sql and execute it
    with current_app.open_resource('scripts/bugtracker.sql') as f:
        db.executescript(f.read().decode('utf8'))


# defines a command line command called init-db that calls the init_db function
@click.command('init-db')
@with_appcontext
def init_db_command():
    """  Clear the existing data and create new tables  """
    init_db()
    # show a success message to the user via terminal
    click.echo('Bug tracker database successfully Initialized.')


# execute external script to import sample data into db
def import_db():
    db = get_db()

    # loads database script from create_sample_data.sql and execute it
    with current_app.open_resource('scripts/create_sample_data.sql') as f:
        db.executescript(f.read().decode('utf8'))


# defines a shell command called import-db to import database sample data
@click.command('import-db')
@with_appcontext
def import_db_command():
    """  Clear the existing data and create new tables  """
    import_db()
    # show a success message to the user via terminal
    click.echo('Bug tracker database sample data successfully imported.')


# Function takes the application instance as a parameter to then register the functions 'close_db' and 'init_db_command'
def init_app(app):
    # Tells Flask to call function 'close_db' when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # add declared commands that can be called with the flask command.
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_db_command)
