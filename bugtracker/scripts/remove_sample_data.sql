----
-- database: bozzbugtracker.db
-- sqlite version: 3
-- Created: 06:23pm on December 21, 2019 (UTC)
-- script file: ./BugTrackingSystem_Remove_SampleData.sql
----
BEGIN TRANSACTION;

delete from bt_issues where issue_id < 29;
delete from bt_users where user_id < 18;
delete from bt_projects where project_id < 6;

;
COMMIT;