-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS student_sessions;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;


-- Users
CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name text,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major text
);

-- Courses
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  major text NOT NULL,
  name text UNIQUE NOT NULL,
  num integer NOT NULL,
  description text,
  credits integer NOT NULL,
  teacher_id bigint REFERENCES users (id) -- One teacher owns many courses
);

-- Sessions
CREATE TABLE sessions (
  id bigserial PRIMARY KEY,
  course_id bigint REFERENCES courses (id), -- One course owns many sessions
  teacher_id bigint REFERENCES users (id), -- One teacher owns many sessions
  section varchar(1) NOT NULL,
  meeting_time timestamptz NOT NULL,
  location varchar(200)
);

-- Students sessions
CREATE TABLE student_sessions (
  id bigserial PRIMARY KEY,
  session_id bigint REFERENCES sessions (id), -- One session owns many student sessions
  student_id bigint REFERENCES users (id) -- One User has many student sessions
);

-- Assignments
CREATE TABLE assignments (
  id bigserial PRIMARY KEY,
  session_id bigint REFERENCES sessions (id), -- One session owns many assignments
  name varchar(50) NOT NULL,
  type varchar(50) NOT NULL,
  points integer NOT NULL,
  due_date date NOT NULL,
  student_sessions_id bigint REFERENCES student_sessions (id) -- One student session owns many Assignments
);
