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
