DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    credits INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    account_type INTEGER NOT NULL
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id)    
    author_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO courses (name, credits, description) VALUES ('Ohjelmoinnin perusteet', 5, 'Opiskelijan ensimmänen kosketus ohjelmointiin.');
INSERT INTO courses (name, credits, description) VALUES ('Ohjelmoinnin jatkokurssi', 5, 'Opiskelijan toinen kosketus ohjelmointiin.');
INSERT INTO courses (name, credits, description) VALUES ('Tietokone ja internet', 5, 'Kurssilla käsitellään vähän kaikenlaista ja kirjoitellaan esseitä 4-6 hengen ryhmissä.');
INSERT INTO courses (name, credits, description) VALUES ('Tietokantojen perusteet', 5, 'Opiskelijan ensimmäinen kosketus tietokantoihin. Kurssilla on käytössä SQLite3.');