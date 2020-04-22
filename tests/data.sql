-- Mock Data For Tests
--Password for the teacher is qwerty
--password for the student is asdfg
--these are just hashed versions of these passwords
INSERT INTO users (id, email, password, name, role, major)
VALUES ('89563', 'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$uGAR1DGg$093c0295e6236f7a69b50b283adf1e167cf0c9f92bf965d9127222e16eff18ea', 'teach', 'teacher', 'CSET'),
       ('43784', 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$gIBqHMMV$36e0b5472a8a74fc632f9a85468b201f887e67dd91898b5fbef53c8e4e9981e8', 'studant', 'student', 'CSET');

INSERT INTO courses (course_number, major, name, description, credits, teacher)
VALUES ('101', 'CSET', 'Web Design', 'We learn and develop code to deploy on the internet', 4, 89563),
       ('301', 'GENEDS', 'Public Speaking', 'In this class you will learn how to plan a speech and speak publically', 4, 53114 );

INSERT INTO session (courses_id, times, name)
VALUES ('1', 'monday', 'A');

INSERT INTO roster (users_id, session_id)
VALUES ('43784', '1');

INSERT INTO assignments (session_id, name, description, date, points)
VALUES ('1', 'Homework', 'homework', '2000-12-31', '5');

INSERT INTO submissions (users_id, assignments_id)
VALUES ('43784', '1');
