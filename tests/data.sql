-- Mock Data For Tests

INSERT INTO majors (name)
VALUES ('CSET'),
        ('ARCH');

INSERT INTO users (email, password, role, name, major)
VALUES ('teacher@stevenscollege.edu', 'qwerty', 'teacher', 'Teacher', 1),
       ('student@stevenscollege.edu', 'asdfgh', 'student', 'Student', 1);
