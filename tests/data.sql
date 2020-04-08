-- Mock Data For Tests

INSERT INTO majors (name)
VALUES  ('CSET'),
        ('WELD'),
        ('CNSA'),
        ('ENG');

INSERT INTO users (email, password, full_name, major_name, role)
VALUES ('teacher@stevenscollege.edu', 'qwerty', 'zach fedor', 'CSET', 'teacher'),
       ('student@stevenscollege.edu', 'asdfgh', 'bob phillp', 'CSET', 'student'),
       ('teacher1@stevengscollege.edu', 'password', 'tim smith', 'WELD', 'teacher'),
       ('teacher2@stevenscollege.edu', 'PASSWORD', 'Ms.Sullivan', 'ENG', 'teacher');

INSERT INTO courses (course_num, course_title, description, credits)
VALUES (180, 'Software Project 2', 'Recreation of the portal', 3),
        (216, 'Technical Writing', 'The practice of proffesional writing',
         3),
         (111, 'Tig Welding Basics', 'Learning how to operate and use the TIG welder',
         3);

INSERT INTO sessions (times, name, room_number, location)
VALUES ('We meet every Tues-Thurs at 1:30 to 2:45', 'ENG-216 D',
307, 'Main campus in Mellor'),
      ('We meet every day at Mon-Fri at 12:00-4:30 except on Wends which we start
        at 12:30', '180', 103, 'GreenField Campus down the hall three doors then
        on your right.' ),
      ('We meet every Wends-Fri ath 12:00 - 3:30', '111', 108,
      'GreenField campus our room is right by the vending machine');
