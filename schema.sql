



DROP TABLE IF EXISTS document;
CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    updated TIMESTAMP NOT NULL
);


