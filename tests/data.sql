-- Mock Data For Tests

INSERT INTO users (email, password,name, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$71PbcIFv$ffc17b1d44fa5ac0b5a9a1707b25e1c69b40a697676a6a30c374a57594b4df99','nancy', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$bhcUxUAk$b08d717a84c93c4d09afe712f0d781b216e5b77a27b9becbf4d535fde22d0e97','quincy', 'student');

-- courses
INSERT INTO courses (major, name, num, description, credits, teacher_id)
VALUES ('CSET', 'Software Project II', 180, 'blaaah', 3, 1),
       ('CSET', 'Web Development', 160, 'web dev lol', 3, 1);

-- sessions
INSERT INTO sessions (course_id, teacher_id, section, meeting_time, location)
VALUES (1, 1, 'A', 'now', 'here'),
       (1, 1, 'B', 'now', 'place st'),
       (2, 1, 'A', 'now', 'road st ave');

-- student sessions
INSERT INTO student_sessions (session_id, student_id)
VALUES (1, 2),
       (2, 2),
       (3, 2);
