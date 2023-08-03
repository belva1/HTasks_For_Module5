/* put database initialization script here */

-- for example
CREATE ROLE owl WITH ENCRYPTED PASSWORD 'mypassword' LOGIN;
COMMENT ON ROLE owl IS 'owl user for tests';

CREATE DATABASE django_project OWNER owl;
COMMENT ON DATABASE django_project IS 'django_project db for tests owned by owl user';
