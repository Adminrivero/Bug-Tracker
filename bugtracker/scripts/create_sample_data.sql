----
-- database: bozzbugtracker.db
-- sqlite version: 3
-- Created: 06:23pm on December 21, 2019 (UTC)
-- script file: ./BugTrackingSystem_Insert_SampleData.sql
----
BEGIN TRANSACTION;

----
-- Sample data dump for projects, a total of 5 rows
----
insert into bt_projects (project_id, project_name, project_desc, start_date, target_end_date, created_by)
values (1, 'Internal Infrastructure', 'Internal Infrastructure, project description here', datetime('now','-150 days'), datetime('now','-30 days'), 'kroberts');
insert into bt_projects (project_id, project_name, project_desc, start_date, target_end_date, created_by)
values (2, 'New Payroll Rollout', 'New Payroll Rollout, project description here', datetime('now','-150 days'), datetime('now','+15 days'), 'kroberts');
insert into bt_projects (project_id, project_name, project_desc, start_date, target_end_date, created_by)
values (3, 'Email Integration', 'Email Integration, project description here', datetime('now','-120 days'), datetime('now','-60 days'), 'kroberts');
insert into bt_projects (project_id, project_name, project_desc, start_date, target_end_date, created_by)
values (4, 'Public Website Operational', 'Public Website Operational, project description here', datetime('now','-60 days'), datetime('now','+30 days'), 'kroberts');
insert into bt_projects (project_id, project_name, project_desc, start_date, target_end_date, created_by)
values (5, 'Employee Satisfaction Survey', 'Employee Satisfaction Survey, project description sample', datetime('now','-30 days'), datetime('now','+60 days'), 'tsuess');

----
-- Sample data dump for users, a total of 17 rows
----
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (1, 'hector', 'rivero', 'admin.rivero@gmail.com', 'admin', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Administrator', null, 'system');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (2, 'Kim', 'Roberts', 'k.roberts@company-domain.com', 'kroberts', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Manager', null, 'admin');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (3, 'Tom', 'Suess', 't.suess@company-domain.com', 'tsuess', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Manager', null, 'admin');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (4, 'Felix', 'Young', 'f.young@company-domain.com', 'fyoung', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Lead', 1, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (5, 'Carla', 'Downing', 'c.downing@company-domain.com', 'cdowning', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Lead', 2, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (6, 'Evan', 'Fanner', 'e.fanner@company-domain.com', 'efanner', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Lead', 3, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (7, 'George', 'Hurst', 'g.hurst@company-domain.com', 'ghurst', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Lead', 4, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (8, 'Irene', 'Jones', 'i.jones@company-domain.com', 'ijones', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Lead', 5, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (9, 'Karen', 'Flores', 'k.london@company-domain.com', 'klondon', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 1, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (10, 'Mark', 'Nile', 'm.nile@company-domain.com', 'mnile', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 1, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (11, 'Jane', 'Kerry', 'j.kerry@company-domain.com', 'jkerry', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 5, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (12, 'Olive', 'Pope', 'o.pope@company-domain.com', 'opope', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 2, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (13, 'Russ', 'Sanders', 'r.sanders@company-domain.com', 'rsanders', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 3, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (14, 'Tucker', 'Uberton', 't.uberton@company-domain.com', 'ruberton', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 3, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (15, 'Vicky', 'Williams', 'v.willaims@company-domain.com', 'vwilliams', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 4, 'kroberts');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (16, 'Scott', 'Tiger', 's.tiger@company-domain.com', 'stiger', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 4, 'tsuess');
insert into bt_users (user_id, first_name, last_name, email, username, password_hash, user_role, assigned_project, created_by)
values (17, 'Yvonne', 'Zeiring', 'y.zeiring@company-domain.com', 'yzeirling', 'pbkdf2:sha256:150000$PyKkLcH9$3adfe0b7dca7d99368ff29558f52ee05a6b27e1fff003a3e9b1d90e5f5145d63', 'Member', 4, 'kroberts');

----
-- Sample data dump for issues, a total of 28 rows
----
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(1, 'Midwest call center servers have no failover due to Conn Creek plant fire','',
6, datetime('now','-80 days'),
3, 6, 'Closed', 'Medium', datetime('now','-73 days'),
'Making steady issue_progress.', datetime('now','-73 days'), '', 'efanner');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(2, 'Timezone ambiguity in some EMEA regions is delaying bulk forwarding to mirror sites','',
6, datetime('now','-100 days'),
3, 14, 'Open', 'Low', datetime('now','-80 days'),
'','','', 'efanner');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(3, 'Some vendor proposals lack selective archiving and region-keyed retrieval sections','',
6, datetime('now','-110 days'),
3, 13, 'Closed', 'Medium', datetime('now','-90 days'),
'', datetime('now','-95 days'), '', 'efanner');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(4, 'Client software licenses expire for Bangalore call center before cutover','',
1, datetime('now','-70 days'),
3, 6, 'Closed', 'High', datetime('now','-60 days'),
'',datetime('now','-66 days'),'Worked with HW, applied patch set.', 'kroberts');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(5, 'Holiday coverage for DC1 and DC3 not allowed under union contract, per acting steward at branch 745','',
1, datetime('now','-100 days'),
3, 13, 'Closed', 'High', datetime('now','-90 days'),
'',datetime('now','-95 days'), 'Worked with HW, applied patch set.', 'kroberts');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(6, 'Review rollout schedule with HR VPs/Directors','',
8, datetime('now','-30 days'),
5, null, 'Closed', 'Medium', datetime('now','-15 days'),
'',datetime('now','-20 days'),'', 'ijones');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(7, 'Distribute translated categories and questions for non-English regions to regional team leads','',
8, datetime('now','-2 days'),
5, 8, 'Open', 'Medium', datetime('now','+10 days'),
'currently beta testing new look and feel','','', 'ijones');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(8, 'Provide survey FAQs to online newsletter group','',
1, datetime('now','-10 days'),
5, 11, 'Open', 'Medium', datetime('now','+20 days'),
'','','', 'tsuess');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(9, 'Need better definition of terms like work group, department, and organization for categories F, H, and M-W','',
1, datetime('now','-8 days'),
5, null, 'Open', 'Low', datetime('now','+15 days'),
'','','', 'tsuess');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(10, 'Legal has asked for better definitions on healthcare categories for Canadian provincial regs compliance','',
1, datetime('now','-10 days'),
5, 11, 'Closed', 'Medium', datetime('now','+20 days'),
'',datetime('now','-1 day'),'', 'tsuess');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(11, 'Action plan review dates conflict with effectivity of organizational consolidations for Great Lakes region','',
1, datetime('now','-9 days'),
5, 11, 'Open', 'Medium', datetime('now','+45 days'),
'','','', 'tsuess');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(12, 'Survey administration consulting firm requires indemnification release letter from HR SVP','',
1, datetime('now','-30 days'),
5, 11, 'Closed', 'Low', datetime('now','-15 days'),
'', datetime('now','-17 days'), '', 'hector86');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(13, 'Facilities, Safety health-check reports must be signed off before capital asset justification can be approved','',
4, datetime('now','-145 days'),
1, 4, 'Closed', 'Medium', datetime('now','-100 days'),
'',datetime('now','-110 days'),'', 'fyoung');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(14, 'Cooling and Power requirements exceed 90% headroom limit -- variance from Corporate requested','',
4, datetime('now','-45 days'),
1, 9, 'Closed', 'High', datetime('now','-30 days'),
'',datetime('now','-35 days'),'', 'fyoung');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(15, 'Local regulations prevent Federal contracts compliance on section 3567.106B','',
4, datetime('now','-90 days'),
1, 10, 'Closed', 'High', datetime('now','-82 days'),
'',datetime('now','-85 days'),'', 'fyoung');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(16, 'Emergency Response plan failed county inspector''s review at buildings 2 and 5','',
4, datetime('now','-35 days'),
1, null, 'Open', 'High', datetime('now','-5 days'),
'','','', 'fyoung');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(17, 'Training for call center 1st and 2nd lines must be staggered across shifts','',
5, datetime('now','-8 days'),
2, 5, 'Closed', 'Medium', datetime('now','+10 days'),
'',datetime('now','-1 day'),'', 'cdowning');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(18, 'Semi-monthly ISIS feed exceeds bandwidth of Mississauga backup site','',
5, datetime('now','-100 days'),
2, 12, 'On-Hold', 'Medium', datetime('now','-30 days'),
'pending info from supplier','','', 'cdowning');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(19, 'Expat exception reports must be hand-reconciled until auto-post phaseout complete','',
5, datetime('now','-17 days'),
2, 12, 'Closed', 'High', datetime('now','+4 days'),
'',datetime('now','-4 days'),'', 'cdowning');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(20, 'Multi-region batch trial run schedule and staffing plan due to directors by end of phase review','',
5, datetime('now'),
2, null, 'Open', 'High', datetime('now','+15 days'),
'','','', 'cdowning');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(21, 'Auditors'' signoff requires full CSB compliance report','',
5, datetime('now','-21 days'),
2, 5, 'Open', 'High', datetime('now','-7 days'),
'','','', 'cdowning');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(22, 'Review security architecture plan with consultant','',
1, datetime('now','-60 days'),
4, 7, 'Closed', 'High', datetime('now','-45 days'),
'',datetime('now','-40 days'),'', 'hector86');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(23, 'Evaluate vendor load balancing proposals against capital budget','',
7, datetime('now','-50 days'),
4, 7, 'Closed', 'High', datetime('now','-45 days'),
'',datetime('now','-43 days'),'', 'ghurst');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(24, 'Some preferred domain names are unavailable in registry','',
7, datetime('now','-55 days'),
4, 15, 'Closed', 'Medium', datetime('now','-45 days'),
'',datetime('now','-50 days'),'', 'ghurst');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(25, 'Establish grid management capacity-expansion policies with ASP','',
7, datetime('now','-20 days'),
4, 16, 'Open', 'Medium', datetime('now','-5 days'),
'','','', 'ghurst');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(26, 'Access through proxy servers blocks some usage tracking tools','',
7, datetime('now','-10 days'),
4, 15, 'Closed', 'High', datetime('now','-5 days'),
'',datetime('now','-1 day'),'', 'ghurst');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(27, 'Phase I stress testing cannot use production network','',
7, datetime('now','-11 days'),
4, 17, 'Open', 'High', datetime('now'),
'','','', 'klondon');
insert into bt_issues (issue_id, issue_subject, issue_desc, identified_by, identified_on, project_id, assigned_to, status, priority, target_resolution_date, issue_progress, actual_resolution_date, resolution_summary, created_by)
values
(28, 'DoD clients must have secure port and must be blocked from others','',
7, datetime('now','-20 days'),
4, 17, 'On-Hold', 'High', datetime('now'),
'Waiting on Security Consultant, this may drag on.','','', 'klondon');

;
COMMIT;