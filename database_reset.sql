DROP TABLE IF EXISTS prets;
CREATE TABLE prets (
	id SERIAL PRIMARY KEY,
	quoi varchar,
	qui varchar,
	statut varchar
);
INSERT INTO prets (quoi, qui, statut) VALUES ('test', 'ppape', 'prete');
