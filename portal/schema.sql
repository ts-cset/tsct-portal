-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS major;

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

--Courses
CREATE TABLE courses (
 courseNumber bigserial PRIMARY KEY,
 name text NOT NULL
 description text
 credits integer NOT NULL
 teacher REFERENCES users(id)
 majorId REFERENCES major(id)
)

--Sessions
CREATE TABLE sessions (
courseId PRIMARY KEY
times text NOT NULL
name text NOT NULL
)

CREATE TABLE major (
userId REFERENCES users(id)
sessionId REFERENCES sessions(courseID)
id PRIMARY KEY 
)
