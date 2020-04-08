-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS roster;

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    last_name varchar(50) NOT NULL,
    first_name varchar(50) NOT NULL,
    major varchar(5) NOT NULL
);

-- Courses
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  course_code varchar(10) NOT NULL,
  course_name text NOT NULL,
  major text NOT NULL,
  description text NOT NULL
  -- Create a one-to-many relationship between teacher users and courses they own
  -- teacher_id bigint REFERENCES users(id) NOT NULL
);

-- Course Sessions
CREATE TABLE sessions (
  id bigserial PRIMARY KEY,
  session_name varchar(1) NOT NULL,
  meeting_days TEXT NOT NULL,
  -- Create a one-to-many relationship between courses and sessions of those courses
  course_id bigint REFERENCES courses(id) NOT NULL
);

-- Roster
-- Create a many-to-many relationship between student users and course sessions
CREATE TABLE roster (
  -- Create a one-to-many relationship between student users and course sessions they belong to
  student_id bigint REFERENCES users(id) NOT NULL,
  -- Create a one-to-many relationship between course sessions and the students that belong to it
  session_id bigint REFERENCES sessions(id) NOT NULL
);
