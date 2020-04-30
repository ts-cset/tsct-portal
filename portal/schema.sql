-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS roster;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

-- Users
CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major text NOT NULL
);

-- Courses
CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    course_number text UNIQUE NOT NULL,
    major text NOT NULL,
    name text NOT NULL,
    description text,
    credits bigint NOT NULL,
    teacher bigint NOT NULL REFERENCES users (id)
);

--session
CREATE TABLE session (
  id bigserial PRIMARY KEY,
  courses_id bigint NOT NULL REFERENCES courses (id),
  times text NOT NULL,
  name varchar(1) NOT NULL
);

--roster
CREATE TABLE roster (
  id bigserial PRIMARY KEY,
  users_id bigint NOT NULL REFERENCES users (id),
  session_id bigint NOT NULL REFERENCES session (id)
);

--assignments
CREATE TABLE assignments (
  id bigserial PRIMARY KEY,
  session_id bigint NOT NULL REFERENCES session (id),
  name text NOT NULL,
  description text NOT NULL,
  date DATE NOT NULL,
  points real NOT NULL
);

--grades
CREATE TABLE grades (
  id bigserial PRIMARY KEY,
  letter varchar(2)
);

--submissions
CREATE TABLE submissions (
  id bigserial PRIMARY KEY,
  users_id bigint NOT NULL REFERENCES users (id),
  assignments_id bigint NOT NULL REFERENCES assignments (id),
  answer text,
  points real DEFAULT 0,
  grades_id bigint DEFAULT 14 REFERENCES grades (id)
);


--assignments and session join table
--CREATE TABLE assignment_sessions (
  --id bigserial PRIMARY KEY,
  --assignments_id bigint NOT NULL REFERENCES assignments (id),
  --session_id bigint NOT NULL REFERENCES session (id)
--);
