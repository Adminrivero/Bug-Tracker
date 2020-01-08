----
-- sqlite3 database: bugtracker.db
-- Created: 11:18pm on December 21, 2019 (UTC)
-- script file: bugtracker.sql 
----
BEGIN TRANSACTION;

----
-- Drop tables if exist
----
DROP TABLE IF EXISTS bt_issues;
DROP TABLE IF EXISTS bt_projects;
DROP TABLE IF EXISTS bt_users;

----
-- Table structure for bt_issues
----
CREATE TABLE 'bt_issues' (
  'issue_id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  'issue_subject' varchar(500) NOT NULL,
  'issue_desc' varchar(4000),
  'identified_by' integer NOT NULL,
  'identified_on' timestamp,
  'project_id' integer NOT NULL,
  'assigned_to' integer,
  'status' varchar(30) NOT NULL,
  'priority' varchar,
  'target_resolution_date' timestamp,
  'issue_progress' TEXT,
  'actual_resolution_date' timestamp DEFAULT NULL,
  'resolution_summary' TEXT,
  'created_on' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'created_by' varchar(255) NOT NULL,
  'modified_on' timestamp,
  'modified_by' varchar(255),
  CONSTRAINT 'bt_issues_identified_by_user_fk' FOREIGN KEY ("identified_by") REFERENCES "bt_users" ("user_id"),
  CONSTRAINT 'bt_issues_assigned_to_user_fk' FOREIGN KEY ("assigned_to") REFERENCES "bt_users" ("user_id"),
  CONSTRAINT 'bt_issues_related_to_project_fk' FOREIGN KEY ("project_id") REFERENCES "bt_projects" ("project_id"),
  CONSTRAINT 'bt_issues_status_ck' CHECK (status in ('Open','On-Hold','Closed')),
  CONSTRAINT 'bt_issues_priority_ck' CHECK (priority in ('High','Medium','Low'))
);

CREATE TRIGGER 'bt_issues_modified_tbu'
BEFORE UPDATE
ON "bt_issues"
FOR EACH ROW
BEGIN
  UPDATE bt_issues
  SET modified_on = CURRENT_TIMESTAMP
  WHERE issue_id = NEW.issue_id;
END;

CREATE TRIGGER 'bt_issues_status_tai'
AFTER INSERT
ON "bt_issues"
FOR EACH ROW
BEGIN
	UPDATE bt_issues
	SET status = 'Open'
	WHERE issue_id = NEW.issue_id AND status Is NULL;
END;

CREATE TRIGGER 'bt_issues_status_closed_tau'
AFTER UPDATE
ON "bt_issues"
FOR EACH ROW
BEGIN
  UPDATE bt_issues
  SET status = 'Closed'
  WHERE issue_id = NEW.issue_id AND actual_resolution_date IS NOT NULL;
END;

----
-- Table structure for bt_projects
----
CREATE TABLE 'bt_projects' (
  'project_id' integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  'project_name' varchar(255) NOT NULL,
  'project_desc' TEXT,
  'start_date' timestamp NOT NULL,
  'target_end_date' timestamp NOT NULL,
  'actual_end_date' timestamp,
  'created_on' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'created_by' varchar(255) NOT NULL,
  'modified_on' timestamp,
  'modified_by' varchar(255),
  CONSTRAINT 'bt_projects_name_uk' UNIQUE ("project_name")
);

CREATE TRIGGER 'bt_projects_modified_tbu'
BEFORE UPDATE
ON "bt_projects"
FOR EACH ROW
BEGIN
  UPDATE bt_projects
  SET modified_on = CURRENT_TIMESTAMP
  WHERE project_id = NEW.project_id;
END;

----
-- Table structure for bt_users
----
CREATE TABLE 'bt_users' (
  'user_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'first_name' varchar(50),
  'last_name' varchar,
  'email' varchar(255),
  'work_phone' varchar(10),
  'username' varchar(255) NOT NULL,
  'password_hash' varchar(255) NOT NULL,
  'user_role' varchar(30) NOT NULL DEFAULT 'Member',
  'account_locked' varchar(1) NOT NULL DEFAULT 'N',
  'assigned_project' integer,
  'created_on' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'created_by' varchar(255) NOT NULL,
  'modified_on' timestamp,
  'modified_by' varchar(255),
  CONSTRAINT 'bt_user_project_fk' FOREIGN KEY ("assigned_project") REFERENCES "bt_projects" ("project_id"),
  CONSTRAINT 'bt_users_username_uk' UNIQUE ("username"),
  CONSTRAINT 'bt_users_user_role_ck' CHECK (user_role in ('Administrator','Manager','Lead','Member')),
  CONSTRAINT 'bt_users_user_assignment_ck' CHECK ( (user_role in ('Lead','Member') and assigned_project is not null) or
(user_role in ('Administrator','Manager') and assigned_project is null) )
);

CREATE TRIGGER 'bt_users_modified_tbu'
BEFORE UPDATE
ON "bt_users"
FOR EACH ROW
BEGIN
	UPDATE bt_users
  SET modified_on = CURRENT_TIMESTAMP
  WHERE user_id = NEW.user_id;
END;

;
COMMIT;