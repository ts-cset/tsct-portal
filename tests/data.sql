-- Mock Data For Tests

INSERT INTO majors (name)
VALUES ('CSET'),
        ('ARCH');

INSERT INTO users (id, email, password, name, role, major)
VALUES (1, 'teacher@stevenscollege.edu', 'qwerty', 'Teacher', 'teacher', 1),
       (2, 'student@stevenscollege.edu', 'asdfgh', 'Student', 'student', 1);
