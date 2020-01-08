from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from bugtracker.auth import login_required, access_forbidden
from bugtracker.db import get_db

bp = Blueprint('project', __name__)


# Only Admin or Manager can create a new project
def check_access_create():
    access_create = False
    if g.user['user_role'] in ['Administrator', 'Manager']:
        access_create = True
    
    return access_create


# Only Admin or Manager can delete a project
def check_access_delete(project_id):
    access_delete = False
    if g.user['user_role'] in ['Administrator', 'Manager']:
        access_delete = True
    
    return access_delete


# shows project list.
@bp.route('/projects')
@login_required
def projects():
    db = get_db()
    where_clause = ""

    if g.user['user_role'] in ['Lead', 'Member']:
        where_clause = " WHERE project_id = '{}'".format(g.user['assigned_project'])

    query = ("SELECT * FROM bt_projects" +
        where_clause +
        " ORDER BY created_on DESC")

    projects = db.execute(query).fetchall()

    access_create = check_access_create()

    return render_template('project/projects.html', projects=projects, access_create=access_create)


# create a new project.
@bp.route('/project/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['inputPName']
        desc = request.form['inputPDesc']
        start_date = request.form['inputSDate']
        target_date = request.form['inputTDate']
        end_date = request.form['inputEDate']

        if not end_date:
            end_date = None

        db = get_db()
        error = None

        if not name:
            error = 'Project name is required.'
        elif not start_date:
            error = 'Project start date is required.'
        elif not target_date:
            error = 'Project target date is required.'
        elif end_date and end_date < start_date:
            error = 'Actual End Date must be same or after Start Date..'
        elif db.execute(
            'SELECT project_id FROM bt_projects WHERE project_name = ?', (name,)
        ).fetchone() is not None:
            error = 'Project {} already exist.'.format(name)

        if error is not None:
            flash(error, 'error')
        else:
            created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'INSERT INTO bt_projects (project_name, project_desc, start_date, target_end_date, actual_end_date, created_on, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, desc, start_date, target_date, end_date, created_on, g.user['username'])
            )
            db.commit()
            return redirect(url_for('project.projects'))

    return render_template('project/create.html')


# utility function to get project by id
def get_project(id, check_owner=True):
    project = get_db().execute(
        'SELECT *'
        ' FROM bt_projects'
        ' WHERE project_id = ?',
        (id,)
    ).fetchone()

    if project is None:
        abort(404, "Project id {0} doesn't exist.".format(id))

    if g.user['user_role'] != 'Administrator':
        if check_owner and project['created_by'] != g.user['username']:
            abort(403, "Access denied, only the administrator or project manager can access")

    return project


# edit a project
@bp.route('/project/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    project = get_project(id)
    access_delete = check_access_delete(id)

    if request.method == 'POST':
        name = request.form['inputPName']
        desc = request.form['inputPDesc']
        start_date = request.form['inputSDate']
        target_date = request.form['inputTDate']
        end_date = request.form['inputEDate']
        error = None
        db = get_db()

        if not end_date or end_date == 'None':
            end_date = None

        if not name:
            error = 'Project name is required.'
        elif not start_date:
            error = 'Project start date is required.'
        elif not target_date:
            error = 'Project target date is required.'

        if error is not None:
            flash(error, 'error')
        else:
            modified_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'UPDATE bt_projects SET project_name = ?, project_desc = ?, start_date = ?, target_end_date = ?, actual_end_date = ?'
                ' , modified_on = ?, modified_by = ?'
                ' WHERE project_id = ?',
                (name, desc, start_date, target_date, end_date, modified_on, g.user['username'], id)
            )
            db.commit()
            return redirect(url_for('project.projects'))

    return render_template('project/edit.html', project=project, access_delete=access_delete)


# delete a project
@bp.route('/project/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_project(id)
    db = get_db()
    db.execute('DELETE FROM bt_projects WHERE project_id = ?', (id,))
    db.commit()

    return redirect(url_for('project.projects'))
