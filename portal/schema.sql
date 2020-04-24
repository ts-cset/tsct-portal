-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS majors CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS roster CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS grades CASCADE;

-- Users
CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password bytea NOT NULL,
    name text,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major varchar(10)
);

-- Majors
CREATE TABLE majors (
  major_id bigserial PRIMARY KEY,
  name varchar(50) UNIQUE NOT NULL,
  description text
);

-- Courses
CREATE TABLE courses (
  course_id bigserial PRIMARY KEY,
  name varchar(50) UNIQUE NOT NULL,
  major varchar(50) NOT NULL,
  description text,
  credits int,
  teacherid bigint NOT NULL
);

ALTER TABLE courses
  ADD CONSTRAINT major_course FOREIGN KEY (major)
    REFERENCES majors(name)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE courses
  ADD CONSTRAINT course_teacher FOREIGN KEY (teacherid)
    REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

-- Sessions
CREATE TABLE sessions (
  id bigserial PRIMARY KEY,
  course_id bigint NOT NULL,
  days varchar(20) NOT NULL,
  class_time time NOT NULL,
  location varchar(50)
);

ALTER TABLE sessions
  ADD CONSTRAINT session_course_name FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

-- Roster
CREATE TABLE roster (
  count bigserial PRIMARY KEY,
  student_id bigint,
  session_id bigint,
  UNIQUE (student_id, session_id)
);

ALTER TABLE roster
  ADD CONSTRAINT student_id FOREIGN KEY (student_id)
    REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE roster
  ADD CONSTRAINT session_id FOREIGN KEY (session_id)
    REFERENCES sessions(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

-- Assignments
CREATE TABLE assignments(
  assignment_id bigserial PRIMARY KEY,
  session_id bigserial,
  name text,
  description text,
  due_date date
);

ALTER TABLE assignments
  ADD CONSTRAINT session FOREIGN KEY (session_id)
  REFERENCES sessions(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE;

-- Grades
CREATE TABLE grades(
  grade_id bigserial PRIMARY KEY,
  student_id bigserial,
  assignment_id bigserial,
  points_received decimal(5,2),
  total_points integer,
  feedback text,
  submission text,
  UNIQUE (grade_id, student_id, assignment_id)
);

ALTER TABLE grades
  ADD CONSTRAINT student FOREIGN KEY (student_id)
  REFERENCES users(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE;

ALTER TABLE grades
  ADD CONSTRAINT assignment FOREIGN KEY (assignment_id)
  REFERENCES assignments(assignment_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE;

INSERT INTO majors (name, description)
  VALUES ('ARCH', 'Architectural Technology'),
          ('AUTO', 'Automotive Technology'),
          ('BUSA', 'Buisiness Administration'),
          ('CSET', 'Computer Software Engineering Technology'),
          ('CARP', 'Carpentry Technology'),
          ('CNSA', 'Computer and Network Systems Administration'),
          ('ELEC', 'Electrical Technology'),
          ('MSON', 'Masonry Technology'),
          ('WELD', 'Welding Technology'),
          ('GEND', 'General Education');
