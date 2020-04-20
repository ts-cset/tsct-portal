-- Mock Data For Tests

INSERT INTO users (email, password, role, last_name, first_name, major)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$YKTR53od$3956727084a9d3470d800ca00005a2258bde5affab208eb9ae211c46a28f575d', 'teacher', 'Fedjona', 'Zachiberto', 'CSET'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$db49oioE$95b37dfa834211006b45fddfa03debdca5d2ccf49486bb7e35af144406d51c8a', 'student', 'Lueklee', 'Kevstice', 'CSET');

INSERT INTO courses (course_code, course_name, major, description, teacher_id)
VALUES ('180', 'Big Software Energy', 'CSET', 'A class that really makes you FEEL like a developer', 1);

INSERT INTO sessions (session_name, meeting_days, course_id)
VALUES ('A', 'MTWThF', 1);

INSERT INTO assignments (name, description, points, course_id)
VALUES ('Big Software', 'You need to create some big software with lots of big software energy', 200, 1),
('Big Software', 'You need to create some big software with lots of big software energy', 200, 1),
('Big Software', 'You need to create some big software with lots of big software energy', 200, 1);

INSERT INTO session_assignments (session_id, assignment_id, due_date)
VALUES (1, 1, '4/25/2020');

-- ID,EMAIL,PASSWORD,NAME,ROLE,MAJOR
-- 42267,duck@stevenscollege.edu,looney,Daffy Duck,teacher,CSET
-- 53114,--email doo@stevenscollege.edu --password snacks --first Scooby --last Doo --role teacher --major ARCH
-- 52502,--email mouse@stevenscollege.edu --password disney --first Minnie --last Mouse --role teacher --major CSET
-- 13041,--email bsimpson041@stevenscollege.edu --password iwillnot --first Bart --last Simpson --role student --major ARCH
-- 36706,--email lsimpson706@stevenscollege.edu --password saxophone --first Lisa --last Simpson --role student --majorCSET
-- 70128,cbrown128@stevenscollege.edu,goodgrief,Charlie Brown,student,CSET
-- 25208,apickles208@stevenscollege.edu,spoiled,Angelica Pickles,student,CSET
-- 48175,bbunny175@stevenscollege.edu,carrots,Bugs Bunny,student,ARCH
-- 50425,fflintstone425@stevenscollege.edu,bowling,Fred Flintstone,student,ARCH

-- heroku run -a desolate-cliffs-09215 flask register --email lsimpson706@stevenscollege.edu --password saxophone --first Lisa --last Simpson --role student --major CSET
