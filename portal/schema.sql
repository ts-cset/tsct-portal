-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;


-- Users
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

-- Courses
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  major text NOT NULL,
  name text UNIQUE NOT NULL,
  num integer UNIQUE NOT NULL,
  description text,
  credits integer NOT NULL,
  teacher_id integer REFERENCES users (id)
)
