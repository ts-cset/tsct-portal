-- Mock Data For Tests

-- INSERT INTO users (email, password, role)
-- VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$YKTR53od$3956727084a9d3470d800ca00005a2258bde5affab208eb9ae211c46a28f575d', 'teacher'),
--        ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$db49oioE$95b37dfa834211006b45fddfa03debdca5d2ccf49486bb7e35af144406d51c8a', 'student');

INSERT INTO courses (name, major, description, teacherid)
VALUES ('ENG 101', 10, 'English Composition: Basic Writing', 42267),
      ('METAL 155', 9, 'Basic metals kinda stuff', 53114),
      ('CSET 180', 4, 'This damn software project', 52502),
      ('DRAW 101', 1, 'Drawing basic buildings', 42267),
      ('ENG 201', 10, 'SECOND YEAR English Composition: Basic Writing', 42267),
      ('METAL 255', 9, 'SECOND YEAR Basic metals kinda stuff', 53114),
      ('CSET 280', 4, 'SECOND YEAR This damn software project', 52502),
      ('DRAW 201', 1, 'SECOND YEAR Drawing basic buildings', 42267);
