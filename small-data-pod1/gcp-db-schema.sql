CREATE EXTENSION IF NOT EXISTS "uuid-ossp";--uid stuff
drop table if exists smalldata; --drop if exists


CREATE TABLE smalldata ( --db schema
	PersonID UUID DEFAULT uuid_generate_v4(),
	Person varchar(255),
	Role varchar(255)
);

-- values init
INSERT INTO smalldata (Person, Role) VALUES
	('Jawad K', 'Docker/DevOps'),
	('Timson', 'NoSQL DBMA'),
	('Zak', 'Cloud Engineer'),
	('William', 'SQL DBMA'),
	('Darren', 'Project Manager'),
	('Jawad C', 'Cloud Engineer');

--display
SELECT * FROM smalldata;