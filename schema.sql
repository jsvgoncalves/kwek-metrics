drop table if exists services;
create table services (
  id INTEGER primary key AUTOINCREMENT,
  name TEXT NOT NULL,
  hwk_url TEXT NOT NULL,
  os_url TEXT NOT NULL,
  token TEXT NOT NULL
);

drop table if exists metrics;
create table metrics (
  id INTEGER primary key AUTOINCREMENT,
  name TEXT NOT NULL,
  display_name TEXT NOT NULL,
  endpoint TEXT NOT NULL,
  tag TEXT NOT NULL,
  unit TEXT NOT NULL,
  conversion REAL NOT NULL,
);
