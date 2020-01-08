import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from bugtracker.db import get_db

# create blueprint 'auth'
bp = Blueprint('auth', __name__)


@bp.route('/')
def route_default():
    return redirect(url_for('auth.login'))


@bp.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


# user login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM bt_users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('dashboard.index'))

        flash(error, 'error')

    return render_template('auth/login.html')


# User registration
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form_data = {'email': '', 'name': '', 'last': '', 'username': ''}
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        last = request.form['last']
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        form_data = request.form.to_dict()

        db = get_db()
        error = None

        if not email:
            error = 'Email name is required.'
        elif not name:
            error = 'First name is required.'
        elif not last:
            error = 'Last name is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not verify:
            error = 'Password confirmation is required.'
        elif not password == verify:
            error = 'Password and confirmation password does not match.'
        elif db.execute(
            'SELECT user_id FROM bt_users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO bt_users (first_name, last_name, email, username, password_hash, user_role, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, last, email, username, generate_password_hash(password), 'Manager', 'Admin')
            )
            db.commit()
            return render_template( 'auth/register.html', success='User created please. <a class="alert-link" href="/login">Log In</a>.')
            #return redirect(url_for('auth.login'))

        flash(error, 'error')

    return render_template('auth/register.html', form=form_data)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM bt_users WHERE user_id = ?', (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.route_default'))


def login_required(view):
    """
    This decorator returns a new view function that wraps the original view it’s applied to. 
    The new function checks if a user is loaded and redirects to the login page otherwise. 
    If a user is loaded the original view is called and continues normally.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


## Errors handler

@bp.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
