-- Mock Data For Tests

INSERT INTO majors (id,name)
VALUES  (1,'CSET'),
        (2,'WELD'),
        (3,'CNSA'),
        (4,'ENG');

INSERT INTO users (id,name, major_id, email, password, role)
VALUES (1,'zach fedor', 1,'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$YKTR53od$3956727084a9d3470d800ca00005a2258bde5affab208eb9ae211c46a28f575d',  'teacher'),
       (2,'bob phillp', 2, 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$db49oioE$95b37dfa834211006b45fddfa03debdca5d2ccf49486bb7e35af144406d51c8a',  'student'),
       (3,'tim smith', 3,'teacher1@stevengscollege.edu', 'password','teacher'),
       (4,'Ms.Sullivan', 4,'teacher2@stevenscollege.edu', 'PASSWORD', 'teacher');

INSERT INTO courses (course_num, course_title, description, credits, teacher_id, major_id)
VALUES (180, 'Software Project 2', 'Recreation of the portal', 3, 1, 1),
        (216, 'Technical Writing', 'The practice of proffesional writing',
         3, 3, 2),
         (111, 'Tig Welding Basics', 'Learning how to operate and use the TIG welder',
         3, 4, 3);

INSERT INTO sessions (times, name, room_number, location, course_id)
VALUES ('We meet every Tues-Thurs at 1:30 to 2:45', 'ENG-216 D',
307, 'Main campus in Mellor', 216),
      ('We meet every day at Mon-Fri at 12:00-4:30 except on Wends which we start
        at 12:30', '180', 103, 'GreenField Campus down the hall three doors then
        on your right.', 180 ),
      ('We meet every Wends-Fri ath 12:00 - 3:30', '111', 108,
      'GreenField campus our room is right by the vending machine', 111);
