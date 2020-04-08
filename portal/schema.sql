
-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS majors;

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name text NOT NULL,
    major REFERENCES majors(id)
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

--Courses
CREATE TABLE courses (
 course_num bigserial PRIMARY KEY,
 course_title text NOT NULL
 description text
 credits integer NOT NULL
 teacher REFERENCES users(id)
 major_Id REFERENCES majors(id)
)

--Sessions
CREATE TABLE sessions (
id PRIMARY KEY,
times text NOT NULL,
name text NOT NULL,
room_number NOT NULL,
location NOT NULL,
course_id REFERENCES courses(id)
)
-- Majors
CREATE TABLE majors (
name NOT NULL
id PRIMARY KEY
)
