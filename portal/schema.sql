
-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
<<<<<<< HEAD

DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS majors CASCADE;





-- Majors
CREATE TABLE majors (
name text NOT NULL,
id bigserial PRIMARY KEY
=======
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS rosters;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS majors;

-- Major
CREATE TABLE majors (
    id bigserial PRIMARY KEY,
    name text NOT NULL
>>>>>>> master
);

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    name text NOT NULL,
    major int REFERENCES majors(id),
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name text NOT NULL,
    major_id bigint REFERENCES majors (id),
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

<<<<<<< HEAD
--Courses
CREATE TABLE courses (
 course_num bigserial PRIMARY KEY,
 course_title text NOT NULL,
 description text,
 credits integer NOT NULL,
 teacher_id bigint REFERENCES users (id),
 major_id bigint REFERENCES majors (id)
);

--Sessions
CREATE TABLE sessions (
id bigserial PRIMARY KEY,
times text NOT NULL,
name text NOT NULL,
room_number integer NOT NULL,
location text NOT NULL,
course_id bigint REFERENCES courses (course_num)
=======
-- Courses
CREATE TABLE courses (
    course_num bigserial PRIMARY KEY,
    credits int NOT NULL,
    course_title text NOT NULL,
    teacher_id int REFERENCES users(id),
    description text,
    major_id int REFERENCES majors(id)
);

-- Assignments
CREATE TABLE assignments (
    id bigserial PRIMARY KEY,
    course_id int REFERENCES courses(course_num)
);

-- Sessions
CREATE TABLE sessions (
    id bigserial PRIMARY KEY,
    name text NOT NULL,
    location text NOT NULL,
    room_number text NOT NULL,
    session_time text NOT NULL,
    course_id int REFERENCES courses(course_num)
);

-- Rosters
CREATE TABLE rosters (
    id bigserial PRIMARY KEY,
    user_id int REFERENCES users(id),
    session_id int REFERENCES sessions(id)
>>>>>>> master
);
