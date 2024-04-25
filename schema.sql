DROP TABLE IF EXISTS Courses CASCADE;

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    credits INTEGER NOT NULL,
    description TEXT
);

INSERT INTO Courses (name, credits, description) VALUES ('Ohjelmoinnin perusteet', 5, 'Opiskelijan ensimmänen kosketus ohjelmointiin.');
INSERT INTO Courses (name, credits, description) VALUES ('Ohjelmoinnin jatkokurssi', 5, 'Opiskelijan toinen kosketus ohjelmointiin.');