drop table if exists service;
create table service (
  id INTEGER primary key AUTOINCREMENT,
  name TEXT NOT NULL,
  hwk_url TEXT NOT NULL,
  os_url TEXT NOT NULL,
  token TEXT NOT NULL
);

drop table if exists metric;
create table metric (
  id INTEGER primary key AUTOINCREMENT,
  name TEXT NOT NULL,
  display_name TEXT NOT NULL,
  endpoint TEXT NOT NULL,
  tag TEXT NOT NULL,
  unit TEXT NOT NULL,
  conversion REAL NOT NULL,
  color TEXT NOT NULL
);
