
-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables

DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS majors CASCADE;





-- Majors
CREATE TABLE majors (
name text NOT NULL,
id bigserial PRIMARY KEY
);

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name text NOT NULL,
    major_id bigint REFERENCES majors (id),
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

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
);
