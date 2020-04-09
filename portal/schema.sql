-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS student_sessions;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;




-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    name varchar(100),
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major varchar(4)
);

-- Courses
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  major varchar(4) NOT NULL,
  name varchar(100) UNIQUE NOT NULL,
  num integer UNIQUE NOT NULL,
  description varchar(1000),
  credits integer NOT NULL,
  teacher_id bigint REFERENCES users (id)
);

-- Session
CREATE TABLE sessions (
  id bigserial PRIMARY KEY,
  course_id bigint REFERENCES courses (id),
  teacher_id bigint REFERENCES users (id),
  section varchar(1) NOT NULL,
  meeting_time timestamptz NOT NULL,
  location varchar(200)
);

-- Students sessions
CREATE TABLE student_sessions (
  id bigserial PRIMARY KEY,
  session_id bigint REFERENCES sessions (id),
  student_id bigint REFERENCES users (id)
)
