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
  teacher_id bigint REFERENCES users (id) -- One teacher owns many courses
);

-- Session
CREATE TABLE sessions (
  course_id bigint REFERENCES courses (id) NOT NULL, -- One course owns many sessions
  teacher_id bigint REFERENCES users (id) NOT NULL, -- One teacher owns many sessions
  section varchar(1) NOT NULL,
  meeting_time time NOT NULL,
  location varchar(200) NOT NULL,
  PRIMARY KEY (course_id, section)
);

-- Students sessions
CREATE TABLE student_sessions (
  id bigserial PRIMARY KEY,
  course_id bigint NOT NULL,
  section varchar(1) NOT NULL,
  FOREIGN KEY  (course_id, section) REFERENCES sessions (course_id, section), -- One session owns many student sessions
  student_id bigint REFERENCES users (id) -- One User has many student sessions
)
