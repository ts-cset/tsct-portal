-- Mock Data For Tests

INSERT INTO majors (id,name)
VALUES  (1,'CSET'),
        (2,'WELD'),
        (3,'CNSA'),
        (4,'ENG');

INSERT INTO users (id,name, major_id, email, password, role)
VALUES (1,'zach fedor', 1,'teacher@stevenscollege.edu', 'qwerty',  'teacher'),
       (2,'bob phillp', 2, 'student@stevenscollege.edu', 'asdfgh',  'student'),
       (3,'tim smith', 3,'teacher1@stevengscollege.edu', 'password','teacher'),
       (4,'Ms.Sullivan', 4,'teacher2@stevenscollege.edu', 'PASSWORD', 'teacher');

INSERT INTO courses (course_num, course_title, description, credits, teacher_id, major_id)
VALUES (180, 'Software Project 2', 'Recreation of the portal', 3, 1, 1),
        (216, 'Technical Writing', 'The practice of proffesional writing',
         3, 3, 2),
         (111, 'Tig Welding Basics', 'Learning how to operate and use the TIG welder',
         3, 4, 3);

INSERT INTO sessions (times, name, room_number, location, course_id)
VALUES ('We meet every Tues-Thurs at 1:30 to 2:45', 'ENG-216-D',
307, 'Main campus in Mellor', 216),
      ('We meet every day at Mon-Fri at 12:00-4:30 except on Wends which we start
        at 12:30', 'CHEM-100-C', 103, 'GreenField Campus down the hall three doors then
        on your right.', 180 ),
      ('We meet every Wends-Fri ath 12:00 - 3:30', 'TIG-A', 108,
      'GreenField campus our room is right by the vending machine', 111);
