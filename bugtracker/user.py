from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from bugtracker.auth import login_required, load_logged_in_user
from bugtracker.db import get_db

bp = Blueprint('user', __name__)


# Only Admin or Manager can create a new user
def check_access_create():
    access_create = False
    if g.user['user_role'] in ['Administrator', 'Manager']:
        access_create = True
    
    return access_create

# Only Admin or Manager can delete users
def check_access_delete():
    access_delete = False
    if g.user['user_role'] in ['Administrator', 'Manager']:
        access_delete = True
    
    return access_delete


# shows users list.
@bp.route('/users')
@login_required
def users():
    db = get_db()
    where_clause = ""

    if g.user['user_role'] == 'Administrator':
        where_clause = " WHERE u.user_role not in ('Administrator')"
    elif g.user['user_role'] == 'Manager':
        where_clause = " WHERE u.user_role not in ('Administrator', 'Manager')"
    elif g.user['user_role'] == 'Lead':
        where_clause = " WHERE u.user_role not in ('Administrator', 'Manager', 'Lead') AND u.assigned_project = '{}'".format(g.user['assigned_project'])
    elif g.user['user_role'] == 'Member':
        where_clause = " WHERE u.username = '{}'".format(g.user['username'])

    query = ("SELECT u.*, p.project_name as `project_name`" +
        " FROM bt_users u left join bt_projects p on u.assigned_project == p.project_id" +
        where_clause +
        " ORDER BY created_on DESC;")
    users = db.execute(query).fetchall()

    access_create = check_access_create()

    return render_template('user/users.html', users=users, access_create=access_create)


# utility function to get projects
def get_projects(check_owner=True):
    where_clause = ""

    if g.user['user_role'] == 'Manager':
        where_clause = " WHERE p.created_by = '{}'".format(g.user['username'])
    elif g.user['user_role'] == 'Lead':
        where_clause = " WHERE p.project_id = '{}'".format(g.user['assigned_project'])

    query = ("SELECT p.project_name, p.project_id" +
    " FROM bt_projects p" +
    where_clause +
    " ORDER BY p.created_on DESC;")

    projects = get_db().execute(query).fetchall()

    if check_owner and not g.user['user_role'] in ['Administrator', 'Manager', 'Lead']:
        abort(403, "Access denied, only administrator and managers can access")

    return projects


# create new user.
@bp.route('/user/create', methods=('GET', 'POST'))
@login_required
def create():
    projects = get_projects()

    if request.method == 'POST':
        first_name = request.form['inputName']
        last_name = request.form['inputLast']
        email = request.form['inputEmail']
        username = request.form['inputUsername']
        user_role = request.form['inputRole']
        assigned_project = request.form['inputProject']

        db = get_db()
        error = None

        if not first_name:
            error = 'User first name is required.'
        elif not last_name:
            error = 'User last name is required.'
        elif not email:
            error = 'User email is required.'
        elif not user_role:
            error = 'User role is required.'
        elif not username:
            error = 'Username is required.'
        elif db.execute(
            'SELECT user_id FROM bt_users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} already exist.'.format(username)

        if error is not None:
            flash(error, 'error')
        else:
            created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'INSERT INTO bt_users (first_name, last_name, email, username, password_hash, user_role, assigned_project, created_on, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (first_name, last_name, email, username, generate_password_hash('password'), user_role, assigned_project, created_on, g.user['username'])
            )
            db.commit()
            return redirect(url_for('user.users'))

    return render_template('user/create.html', projects=projects)


# utility function to get user by id
def get_user(id, check_login=True):
    user = get_db().execute(
        'SELECT *'
        ' FROM bt_users'
        ' WHERE user_id = ?',
        (id,)
    ).fetchone()

    if user is None:
        abort(404, "User id {0} doesn't exist.".format(id))

    if not g.user['user_role'] in ['Administrator', 'Manager']:
        if check_login and user['user_id'] != g.user['user_id']:
            abort(403, "Access denied, only administrator and managers can manage user accounts")

    return user


# edit user
@bp.route('/user/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    user = get_user(id)
    access_delete = check_access_delete()
    projects = get_projects()

    if request.method == 'POST':
        first_name = request.form['inputName']
        last_name = request.form['inputLast']
        email = request.form['inputEmail']
        user_role = request.form['inputRole']
        assigned_project = None
        if not user_role in ['Administrator', 'Manager']:
            assigned_project = request.form['inputProject']

        error = None
        db = get_db()

        if not first_name:
            error = 'User first name is required.'
        elif not last_name:
            error = 'User last name is required.'
        elif not email:
            error = 'User email is required.'
        elif not user_role:
            error = 'User role is required.'

        if error is not None:
            flash(error, 'error')
        else:
            modified_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'UPDATE bt_users SET first_name = ?, last_name = ?, email = ?, user_role = ?, assigned_project = ?'
                ' , modified_on = ?, modified_by = ?'
                ' WHERE user_id = ?',
                (first_name, last_name, email, user_role, assigned_project, modified_on, g.user['username'], id)
            )
            db.commit()
            return redirect(url_for('user.users'))

    return render_template('user/edit.html', projects=projects, user=user, access_delete=access_delete)


# delete user
@bp.route('/user/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()

    if check_access_delete():
        db.execute('DELETE FROM bt_users WHERE user_id = ?', (id,))
        db.commit()
    else:
        abort(403, "Access denied, only administrator or managers can delete an user")

    return redirect(url_for('user.users'))


# user profile
@bp.route('/user/profile', methods=('GET', 'POST'))
@login_required
def profile():
    user = get_user(g.user['user_id'])

    if request.method == 'POST':
        first_name = request.form['inputName']
        last_name = request.form['inputLast']
        email = request.form['inputEmail']

        error = None
        db = get_db()

        if not first_name:
            error = 'User first name is required.'
        elif not last_name:
            error = 'User last name is required.'
        elif not email:
            error = 'User email is required.'

        if error is not None:
            flash(error, 'error')
        else:
            modified_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'UPDATE bt_users SET first_name = ?, last_name = ?, email = ?, modified_on = ?, modified_by = ?'
                ' WHERE user_id = ?',
                (first_name, last_name, email, modified_on, g.user['username'], g.user['user_id'])
            )
            db.commit()
            load_logged_in_user()
            user = get_user(g.user['user_id'])
            #return redirect(url_for('dashboard.index'))

    return render_template('user/profile.html', user=user)


# User change password
@bp.route('/change_password', methods=('GET', 'POST'))
def change_pass():
    if request.method == 'POST':
        current = request.form['inputCPass']
        new = request.form['inputNPass']
        verify = request.form['inputVPass']

        db = get_db()
        error = None

        if not current:
            error = 'Current password is required.'
        elif not new:
            error = 'New password is required.'
        elif not verify:
            error = 'Password confirmation is required.'
        elif not new == verify:
            error = 'Password and confirmation password does not match.'
        elif not check_password_hash(g.user['password_hash'], current):
            error = 'Incorrect current password. Please try again.'

        if error is None:
            db.execute(
                'UPDATE bt_users SET password_hash = ?'
                ' WHERE user_id = ?',
                (generate_password_hash(new), g.user['user_id'])
            )
            db.commit()
            return redirect(url_for('user.profile'))

        flash(error, 'error')

    return render_template('user/change_password.html')