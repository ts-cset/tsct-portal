-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS grades;
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
    name varchar(100),
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major varchar(4)
);

-- Courses
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  major varchar(4) NOT NULL,
  name varchar(100) UNIQUE NOT NULL,
  num integer NOT NULL,
  description varchar(1000),
  credits integer NOT NULL,
  teacher_id bigint REFERENCES users (id) -- One teacher owns many courses
  ON DELETE CASCADE
);

-- Session
CREATE TABLE sessions (
  course_id bigint REFERENCES courses (id) ON DELETE CASCADE NOT NULL , -- One course owns many sessions
  teacher_id bigint REFERENCES users (id) ON DELETE CASCADE NOT NULL , -- One teacher owns many sessions
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
  FOREIGN KEY  (course_id, section) REFERENCES sessions (course_id, section) ON DELETE CASCADE, -- One session owns many student sessions
  student_id bigint REFERENCES users (id) -- One User has many student sessions
  ON DELETE CASCADE
);

-- Assignments
CREATE TABLE assignments (
  id bigserial PRIMARY KEY,
  course_id bigint NOT NULL,
  section varchar(1) NOT NULL,
  FOREIGN KEY  (course_id, section) REFERENCES sessions (course_id, section) ON DELETE CASCADE, -- One session owns many assignments
  name varchar(50) NOT NULL,
  type varchar(50) NOT NULL,
  points integer NOT NULL,
  due_date date NOT NULL,
  student_sessions_id bigint REFERENCES student_sessions (id) -- One student session owns many Assignments
  ON DELETE CASCADE
);

-- Grades
CREATE TABLE grades (
  id bigserial PRIMARY KEY,
  student_session_id bigint REFERENCES student_sessions (id) NOT NULL,
  assignment_id integer REFERENCES assignments (id) NOT NULL,
  points_earned integer NOT NULL
);
