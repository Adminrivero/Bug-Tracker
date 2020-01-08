from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bugtracker.auth import login_required
from bugtracker.db import get_db

bp = Blueprint('dashboard', __name__)

# index shows user dashboard.
@bp.route('/index')
@login_required
def index():
    db = get_db()
    dash_stats = dict()

    dash_stats['users_total'] = db.execute(
            "SELECT count(*) from bt_users where user_role <> 'Administrator'"
        ).fetchone()
    dash_stats['projects_total'] = db.execute(
            "SELECT count(*) from bt_projects"
        ).fetchone()
    dash_stats['issues_total'] = db.execute(
            "SELECT count(*) from bt_issues"
        ).fetchone()
    dash_stats['issues_by_status'] = db.execute(
            'select SUM(CASE When status="Open" Then 1 Else 0 End ) as `sum_open`,'
            ' SUM(CASE When status="On-Hold" Then 1 Else 0 End ) as `sum_on_hold`,'
            ' SUM(CASE When status="Closed" Then 1 Else 0 End ) as `sum_closed`'
            ' from bt_issues;'
        ).fetchone()
    dash_stats['issues_stats'] = db.execute(
            'select SUM(CASE When target_resolution_date < DATE("now") AND status = "Open" Then 1 Else 0 End ) as `sum_overdue`,'
            ' SUM(CASE When assigned_to is NULL Then 1 Else 0 End ) as `sum_unassigned`'
            ' from bt_issues;'
        ).fetchone()

    query = ("SELECT i.issue_id, i.issue_subject, i.priority, i.target_resolution_date," +
        " p.project_name, ua.first_name || ' ' || ua.last_name AS assignee" +
        " FROM bt_issues i " +
        " INNER JOIN bt_projects p ON p.project_id = i.project_id " +
        " LEFT JOIN bt_users ui ON ui.user_id = i.identified_by" +
        " LEFT JOIN bt_users ua ON ua.user_id = i.assigned_to" +
        " WHERE i.target_resolution_date < DATE('now') AND i.status = 'Open'" +
        " ORDER BY i.issue_id DESC")

    issues_overdue = db.execute(query).fetchall()

    return render_template('dashboard/index.html', dash_stats=dash_stats, issues_overdue=issues_overdue)


