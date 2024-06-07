DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS suggestions CASCADE;
DROP TABLE IF EXISTS enrollments CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    account_type INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    credits INTEGER NOT NULL,
    description TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id), 
    author_id INTEGER REFERENCES users(id),
    rating INTEGER NOT NULL,
    content VARCHAR(520) NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE suggestions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    credits INTEGER NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    user_id INTEGER REFERENCES users(id),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_course_user UNIQUE (course_id, user_id)
);

INSERT INTO users (username, password, account_type) VALUES ('aappo', 'scrypt:32768:8:1$9dSFfZSyzkeRQOnU$b2c82fac6ecd1ecff802b97f93003bc9cd4f30821fc82365ee5480942e8479901fece5ca8a2c55eecd23be339846803638d6380adfe548c42afd7a7089cab83f', 1);

INSERT INTO courses (name, credits, description) VALUES ('Ohjelmoinnin perusteet', 5, 'Opiskelijan ensimmänen kosketus ohjelmointiin.');
INSERT INTO courses (name, credits, description) VALUES ('Ohjelmoinnin jatkokurssi', 5, 'Opiskelijan toinen kosketus ohjelmointiin.');
INSERT INTO courses (name, credits, description) VALUES ('Tietokone ja internet', 5, 'Kurssilla käsitellään vähän kaikenlaista ja kirjoitellaan esseitä 4-6 hengen ryhmissä.');
INSERT INTO courses (name, credits, description) VALUES ('Tietokantojen perusteet', 5, 'Opiskelijan ensimmäinen kosketus tietokantoihin. Kurssilla on käytössä SQLite3.');

INSERT INTO comments (course_id, author_id, rating, content) VALUES (1, 1, 4, 'Kurssi oli mielestäni onnistunut, sillä jady jada.');
INSERT INTO comments (course_id, author_id, rating, content) VALUES (1, 1, 3, 'Oli tylsää');