-- Mock Data For Tests

-- Users
INSERT INTO users (id, email, password, name, role, major)
VALUES (1, 'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$71PbcIFv$ffc17b1d44fa5ac0b5a9a1707b25e1c69b40a697676a6a30c374a57594b4df99', 'ms teacher', 'teacher', 'CSET'),
       (2, 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$bhcUxUAk$b08d717a84c93c4d09afe712f0d781b216e5b77a27b9becbf4d535fde22d0e97', 'kyle', 'student', 'CSET'),
       (42267, 'duck@stevenscollege.edu', 'looney', 'Daffy Duck', 'teacher', 'WELD'),
       (50425, 'fflintstone425@stevenscollege.edu', 'bowling', 'Fred Flintstone', 'student', 'ARCH'),
       (13041, 'bsimpson041@stevenscollege.edu', 'iwillnot', 'Bart Simpson', 'student', 'ARCH');
-- Courses
INSERT INTO courses (major, name, num, description, credits, teacher_id)
VALUES ('CSET', 'Software Project II', 180, 'blaaah', 3, 1),
       ('CSET', 'Security and Ethics', 170, 'delete me', 3, 1),
       ('CSET', 'Web Development', 160, 'web dev lol', 3, 2),
       ('Welding', 'Metal', 105, 'weld', 3, 42267);

-- Sessions
INSERT INTO sessions (course_id, teacher_id, section, meeting_time, location)
VALUES (1, 1, 'A', 'now', 'first st PA'),
       (2, 1, 'B', 'now', 'tenth st CA'),
       (3, 42267, 'C', 'now', 'shop');

-- Student Sessions
INSERT INTO student_sessions (session_id, student_id)
VALUES (1, 2),
       (2, 2),
       (2, 13041),
       (3, 50425);

-- Assignments
INSERT INTO assignments (session_id, name, type, points, due_date, student_sessions_id)
VALUES (1, 'homework', 'paper', 10, 'now', 1),
       (2, 'website', 'final', 50, 'now', 2),
       (1, 'application', 'final', 100, 'now', 1),
       (1, 'homework', 'paper', 10, 'now', 3),
       (3, 'weld panel', 'classwork', 25, 'now', 4);
