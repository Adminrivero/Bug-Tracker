from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from bugtracker.auth import login_required, access_forbidden
from bugtracker.db import get_db

bp = Blueprint('issue', __name__)


# shows list of issues
@bp.route('/issues')
@login_required
def issues():
    db = get_db()
    where_clause = ""

    if g.user['user_role'] in ['Lead', 'Member']:
        where_clause = " WHERE i.assigned_to = '{}' OR i.project_id = '{}'".format(g.user['user_id'], g.user['assigned_project'])

    query = ("SELECT i.issue_id, i.issue_subject, i.identified_on, i.status, i.priority, i.target_resolution_date," +
        " i.issue_progress, i.actual_resolution_date, ui.first_name || ' ' || ui.last_name AS identified_by," +
        " p.project_name, ua.first_name || ' ' || ua.last_name AS assigned_to" +
        " FROM bt_issues i " +
        " INNER JOIN bt_projects p ON p.project_id = i.project_id " +
        " LEFT JOIN bt_users ui ON ui.user_id = i.identified_by" +
        " LEFT JOIN bt_users ua ON ua.user_id = i.assigned_to" +
        where_clause +
        " ORDER BY i.issue_id DESC")

    issues = db.execute(query).fetchall()

    return render_template('issue/issues.html', issues=issues)


# utility function to get projects
def get_projects(check_owner=True):
    where_clause = ""

    if g.user['user_role'] == 'Manager':
        where_clause = " WHERE p.created_by = '{}'".format(g.user['username'])
    elif g.user['user_role'] in ['Lead', 'Member']:
        where_clause = " WHERE p.project_id = '{}'".format(g.user['assigned_project'])

    query = ("SELECT p.project_name, p.project_id" +
    " FROM bt_projects p" +
    where_clause +
    " ORDER BY p.created_on DESC;")

    projects = get_db().execute(query).fetchall()

    return projects


# utility function to get users
def get_users(check_login=True):
    where_clause = " WHERE u.user_role not in ('Administrator', 'Manager')"

    if g.user['user_role'] == 'Lead':
        where_clause += " AND u.assigned_project = '{}'".format(g.user['assigned_project'])
    elif g.user['user_role'] == 'Member':
        where_clause += " AND u.user_id = '{}'".format(g.user['user_id'])

    query = ("SELECT u.first_name, u.last_name, u.user_id" +
    " FROM bt_users u" +
    where_clause +
    " ORDER BY u.first_name DESC;")

    users = get_db().execute(query).fetchall()

    return users


# create issue
@bp.route('/issue/create', methods=('GET', 'POST'))
@login_required
def create():
    projects = get_projects()
    users = get_users()

    if request.method == 'POST':
        issue_subject = request.form['inpuSubject']
        issue_desc = request.form['inputDesc']
        issue_project = request.form['inputProject']
        issue_ident_by = request.form['inputIdentBy']
        issue_ident_on = request.form['inputIdentOn']
        issue_assigned_to = request.form['inputAssigned']
        issue_status = request.form['inputStatus']
        issue_priority = request.form['inputPriority']
        issue_target_date = request.form['inputDueDate']
        issue_progress = request.form['inputProgress']
        issue_actual_date = request.form['inputEndDate']
        issue_end_summary = request.form['inputEndSum']

        if not issue_target_date:
            issue_target_date = None
        if not issue_actual_date:
            issue_actual_date = None

        db = get_db()
        error = None

        if not issue_subject:
            error = 'Issue summary is required.'
        elif not issue_project:
            error = 'Related project is required.'
        elif not issue_ident_by:
            error = 'Identified by is required.'
        elif not issue_ident_on:
            error = 'Identified date is required.'
        elif not issue_status:
            error = 'Issue status is required.'
        elif not issue_priority:
            error = 'Issue priority is required.'
        elif issue_actual_date and issue_actual_date < issue_target_date:
            error = 'Actual resolution date must be same or after to target resolution date.'

        if error is not None:
            flash(error, 'error')
        else:
            created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'INSERT INTO bt_issues (issue_subject, issue_desc, project_id, identified_by, identified_on, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_on, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (issue_subject, issue_desc, issue_project, issue_ident_by, issue_ident_on, issue_assigned_to, issue_status, issue_priority, issue_target_date, issue_progress, issue_actual_date, issue_end_summary, created_on, g.user['username'])
            )
            db.commit()
            return redirect(url_for('issue.issues'))

    return render_template('issue/create.html', projects=projects, users=users)


# check access to delete an issue
def check_access_delete(issue_id):
    access_delete = True
    issue = get_db().execute(
        'SELECT *'
        ' FROM bt_issues'
        ' WHERE issue_id = ?',
        (issue_id,)
    ).fetchone()

    if g.user['user_role'] in ['Member', 'Lead']:
        if issue['created_by'] != g.user['username']:
            access_delete = False
    
    return access_delete


# utility function to get issue by id
def get_issue(id, check_login=True):

    issue = get_db().execute(
        'SELECT *'
        ' FROM bt_issues'
        ' WHERE issue_id = ?',
        (id,)
    ).fetchone()

    if issue is None:
        abort(404, "Issue id {0} doesn't exist.".format(id))

    if check_login and g.user['user_role'] == 'Member':
        if issue['assigned_to'] != g.user['user_id']:
            abort(403, "Access denied, only administrator and managers can manage user accounts")

    if check_login and g.user['user_role'] == 'Lead':
        if issue['assigned_to'] != g.user['user_id'] and issue['created_by'] != g.user['username']:
            abort(403, "Access denied, only administrator and managers can manage user accounts")

    return issue


# edit issue
@bp.route('/issue/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    issue = get_issue(id)
    access_delete = check_access_delete(id)
    projects = get_projects()
    users = get_users()

    if request.method == 'POST':
        issue_subject = request.form['inpuSubject']
        issue_desc = request.form['inputDesc']
        issue_project = request.form['inputProject']
        issue_ident_by = request.form['inputIdentBy']
        issue_ident_on = request.form['inputIdentOn']
        issue_assigned_to = request.form['inputAssigned']
        issue_status = request.form['inputStatus']
        issue_priority = request.form['inputPriority']
        issue_target_date = request.form['inputDueDate']
        issue_progress = request.form['inputProgress']
        issue_actual_date = request.form['inputEndDate']
        issue_end_summary = request.form['inputEndSum']

        if not issue_target_date or issue_target_date == 'None':
            issue_target_date = None
        if not issue_actual_date or issue_actual_date == 'None':
            issue_actual_date = None

        db = get_db()
        error = None

        if not issue_subject:
            error = 'Issue summary is required.'
        elif not issue_project:
            error = 'Related project is required.'
        elif not issue_ident_by:
            error = 'Identified by is required.'
        elif not issue_ident_on:
            error = 'Identified date is required.'
        elif not issue_status:
            error = 'Issue status is required.'
        elif not issue_priority:
            error = 'Issue priority is required.'
        elif issue_actual_date and issue_actual_date < issue_target_date:
            error = 'Actual resolution date must be same or after to target resolution date.'

        if error is not None:
            flash(error, 'error')
        else:
            modified_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute(
                'UPDATE bt_issues SET issue_subject = ?, issue_desc = ?, project_id = ?, identified_by = ?,'
                ' identified_on = ?, assigned_to = ?, status = ?, priority = ?, target_resolution_date = ?,'
                ' issue_progress = ?, actual_resolution_date = ?, resolution_summary = ?, modified_on = ?, modified_by = ?'
                ' WHERE issue_id = ?',
                (issue_subject, issue_desc, issue_project, issue_ident_by, issue_ident_on, issue_assigned_to, issue_status, issue_priority, issue_target_date, issue_progress, issue_actual_date, issue_end_summary, modified_on, g.user['username'], id)
            )
            db.commit()
            return redirect(url_for('issue.issues'))

    return render_template('issue/edit.html', issue=issue, access_delete=access_delete, projects=projects, users=users)


# delete issue
@bp.route('/issue/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()

    if check_access_delete(id):
        db.execute('DELETE FROM bt_users WHERE user_id = ?', (id,))
        db.commit()
    else:
        abort(403, "Access denied, only administrator or managers can delete an user")

    return redirect(url_for('user.users'))