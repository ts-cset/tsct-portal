-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'qwerty', 'teacher'),
       ('student@stevenscollege.edu', 'asdfgh', 'student');

-- courses
INSERT INTO courses (major, name, num, description, credits)
VALUES ('CSET', 'Software Project II', 180, 'blaaah', 3),
       ('CSET', 'Web Development', 160, 'web dev lol', 3);
