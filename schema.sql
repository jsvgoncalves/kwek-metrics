drop table if exists services;
create table services (
  id INTEGER primary key AUTOINCREMENT,
  -- ENCRYPTED
  -- name TEXT NOT NULL,
  name TEXT NOT NULL,
  -- url TEXT NOT NULL,
  url TEXT NOT NULL,
  -- token TEXT NOT NULL,
  token TEXT NOT NULL
);

drop table if exists metrics;
create table metrics (
  id INTEGER primary key AUTOINCREMENT,
  -- ENCRYPTED
  -- name TEXT NOT NULL,
  name TEXT NOT NULL,
  -- value TEXT NOT NULL,
  query TEXT NOT NULL
);