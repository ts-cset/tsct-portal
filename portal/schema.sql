-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS majors CASCADE;
DROP TABLE IF EXISTS courses CASCADE;

-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password bytea NOT NULL,
    name text,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major varchar(10)
);

CREATE TABLE majors (
  major_id bigserial PRIMARY KEY,
  name varchar(50),
  description text
);

CREATE TABLE courses (
  course_id bigserial PRIMARY KEY,
  name varchar(50),
  major bigint NOT NULL,
  description text,
  teacherId bigint NOT NULL
);

ALTER TABLE courses
  ADD CONSTRAINT major_course FOREIGN KEY (major)
    REFERENCES majors(major_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE courses
  ADD CONSTRAINT course_teacher FOREIGN KEY (teacherId)
    REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE cascade;
