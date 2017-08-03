\disconnect;
drop database predictatron;
CREATE DATABASE predictatron WITH ENCODING 'UNICODE' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;
grant all on database predictatron to predictuser;
\connect predictatron;
create table snapshot (
    id serial primary key, 
    snapshot_date date,
    snapshot_name varchar(255),
    backlog_small int,
    backlog_medium int,
    backlog_large int,
    backlog_xl int,
    history_weeks int,
    history_small int,
    history_medium int,
    history_large int,
    history_xl int);
grant all on snapshot to predictuser;
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-06-06','NMA Sprint 0',5,5,9,1,1,9,7,4,0);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-06-13','NMA Sprint 1',5,8,9,2,2,15,8,8,0);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-06-20','NMA Sprint 2',7,16,14,3,3,21,14,13,0);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-06-27','NMA Sprint 3',5,14,15,6,4,27,21,17,0);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-07-04','NMA Sprint 4',5,13,13,3,5,31,28,21,3);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-07-11','NMA Sprint 5',5,12,13,6,6,34,33,26,5);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-07-18','NMA Sprint 6',5,12,14,5,7,38,36,29,6);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-07-25','NMA Sprint 7',6,10,13,5,8,40,42,31,6);
insert into snapshot (snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl,
    history_weeks, history_small, history_medium, history_large, history_xl) 
    values('2017-08-01','NMA Sprint 8',7,11,13,7,9,43,49,33,7);

create table epic (
    epic_id serial primary key, 
    snapshot_date date,
    goal_period int,
    epic_title varchar(200),
    status varchar(12),
    kanban_small int, 
    kanban_medium int,
    kanban_large int,
    kanban_xl int);
grant all on epic to predictuser;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO predictuser;
insert into epic (snapshot_date, goal_period, epic_title, status, kanban_small, kanban_medium, kanban_large, kanban_xl)
    values('2017-04-12', 1, 'The Awesome Test Epic', 'green', 10, 6, 2, 0);