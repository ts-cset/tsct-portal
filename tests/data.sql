-- Mock Data For Tests

INSERT INTO users (id, email, password, name, role, major)
VALUES (0001, 'teacher@stevenscollege.edu', '$2b$12$xVtl1ZGJBEW4gxQOm9UzW.P.UOq/cR7/TEv.G3l3x.TmV29yX8a5y', 'Test Teacher', 'teacher', 'ARCH'),
       (0002, 'student@stevenscollege.edu', '$2b$12$PE/vM8jOb6Og84zdJ9GvKe8177OZ8EhMRzEwAONF1R8R6qeJ6PAsm', 'Test Student', 'student', 'CSET'),
       (0003, 'teacher2@stevenscollege.edu', '$2b$12$xVtl1ZGJBEW4gxQOm9UzW.P.UOq/cR7/TEv.G3l3x.TmV29yX8a5y', 'Test Teacher 2', 'teacher', 'AUTO'),
       (0004, 'student2@stevenscollege.edu', '$2b$12$PE/vM8jOb6Og84zdJ9GvKe8177OZ8EhMRzEwAONF1R8R6qeJ6PAsm', 'Test Student 2', 'student', 'BUSA'),
       (0005, 'student3@stevenscollege.edu', '$2b$12$PE/vM8jOb6Og84zdJ9GvKe8177OZ8EhMRzEwAONF1R8R6qeJ6PAsm', 'Test Student 3', 'student', 'CSET');

INSERT INTO courses (name, major, description, credits, teacherid)
VALUES ('ENG 101', 'GEND', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 3, 0003),
      ('METAL 155', 'WELD', 'Basic metals kinda stuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 3, 0001),
      ('CSET 180', 'CSET', 'This damn software project Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 2, 0001),
      ('DRAW 101', 'ARCH', 'Drawing basic buildings Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 3, 0003),
      ('ENG 201', 'GEND', 'SECOND YEAR English Composition Basic Writing', 3, 0001),
      ('METAL 255', 'WELD', 'SECOND YEAR Basic metals kinda stuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 2, 0003),
      ('CSET 280', 'CSET', 'SECOND YEAR This damn software projec Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 3, 0003),
      ('DRAW 201', 'ARCH', 'SECOND YEAR Drawing basic building Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 3, 0001);

INSERT INTO sessions ( course_id, days, class_time, location)
VALUES ( 3, 'M/W/F', '9:00am', 'Main Campus'),
      ( 2, 'T/Th', '10:30am', 'Main Campus'),
      ( 8, 'T', '6:00pm', 'Main Campus'),
      ( 7, 'M/W/F', '8:15am', 'Branch Campus'),
      ( 1, 'T/Th', '1:30pm', 'Main Campus'),
      ( 1, 'W/F', '12:00pm', 'Branch Campus'),
      ( 6, 'M', '6:00pm', 'Main Campus'),
      ( 8, 'T', '6:00pm', 'Main Campus'),
      ( 7, 'M/W/F', '8:15am', 'Branch Campus'),
      ( 8, 'T/Th', '1:30pm', 'Main Campus'),
      ( 5, 'W/F', '12:00pm', 'Branch Campus');


INSERT INTO assignments (session_id, name, description, due_date)
VALUES (1, 'Exam_1', 'Chapter 1 Exam:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-04-28'),
      (1, 'Exam_2', 'Chapter 2 Exam:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-05-03'),
      (2, 'Essay', 'Biographical Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-05-02'),
      (2, 'Essay', 'Persuasive Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-08-09'),
      (3, 'Lab', 'Some Things:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-04-29'),
      (3, 'Lab', 'Crazy Experiment Details:Lorem ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
        aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
        sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.', '2020-06-16'),
      (4, 'Exam_2', 'Chapter 2 Exam', '2020-05-03'),
      (4, 'Essay', 'Biographical Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-05-02'),
      (5, 'Essay', 'Persuasive Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-08-09'),
      (5, 'Lab', 'Some Things:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-04-29'),
      (6, 'Lab', 'Crazy Experiment Details:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-06-16'),
      (6, 'Exam_2', 'Chapter 2 Exam:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-05-03'),
      (7, 'Essay', 'Biographical Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-05-02'),
      (7, 'Essay', 'Persuasive Essay:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-08-09'),
      (8, 'Lab', 'Some Things:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-04-29'),
      (8, 'Lab', 'Crazy Experiment Details:Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-06-16');

INSERT INTO roster (student_id, session_id)
VALUES (4, 1),
        (4, 3),
        (4, 5),
        (4, 7),
        (2, 2),
        (2,4),
        (2,6),
        (2,1),
        (2, 7),
        (5, 1),
        (5, 3),
        (5, 4),
        (5, 7),
        (5, 8);

INSERT INTO grades (student_id, assignment_id, points_received, total_points, feedback, submission)
VALUES (4, 1, 10, 20, 'good job', 'my submission'),
        (4, 2, 13, 30, 'not so good', 'my submission'),
        (4, 5, 20, 25, 'whatever', 'whatever'),
        (4, 7, 10, 10, 'good job', 'my submission'),
        (4, 9, 13, 20, 'not so good', 'my submission'),
        (4, 12, 20, 30, 'whatever', 'whatever'),
        (4, 13, 20, 25, 'whatever', 'whatever'),
        (4, 15, 10, 10, 'good job', 'my submission'),
        (4, 16, 13, 20, 'not so good', 'my submission'),
        (2, 1, 20, 20, 'whatever', 'whatever'),
        (2, 2, 20, 30, 'whatever', 'whatever'),
        (2, 3, 10, 10, 'good job', 'my submission'),
        (2, 4, 13, 20, 'not so good', 'my submission'),
        (2, 5, 20, 25, 'whatever', 'whatever'),
        (2, 11, 13, 20, 'not so good', 'my submission'),
        (2, 13, 20, 25, 'whatever', 'whatever'),
        (2, 14, 20, 25, 'whatever', 'whatever'),
        (5, 1, 13, 20, 'not so good', 'my submission'),
        (5, 2, 20, 30, 'whatever', 'whatever'),
        (5, 5, 10, 25, 'good job', 'my submission'),
        (5, 6, 13, 20, 'not so good', 'my submission'),
        (5, 9, 20, 20, 'whatever', 'whatever'),
        (5, 11, 20, 20, 'whatever', 'whatever'),
        (5, 12, 10, 30, 'good job', 'my submission'),
        (5, 13, 13, 25, 'not so good', 'my submission'),
        (5, 15, 10, 10, 'whatever', 'whatever');
