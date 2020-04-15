-- Mock Data For Tests

INSERT INTO users (id, email, password, name, role, major)
VALUES (0001, 'teacher@stevenscollege.edu', 'qwerty', 'test', 'teacher', 1),
       (0002, 'student@stevenscollege.edu', 'password', 'test', 'student', 10);

INSERT INTO courses (name, major, description, teacherid)
VALUES ('ENG 101', 'GEND', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0001),
      ('METAL 155', 'WELD', 'Basic metals kinda stuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0001),
      ('CSET 180', 'CSET', 'This damn software project Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0001),
      ('DRAW 101', 'ARCH', 'Drawing basic buildings Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0001),
      ('ENG 201', 'GEND', 'SECOND YEAR English Composition Basic Writing', 0002),
      ('METAL 255', 'WELD', 'SECOND YEAR Basic metals kinda stuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0002),
      ('CSET 280', 'CSET', 'SECOND YEAR This damn software projec Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0002),
      ('DRAW 201', 'ARCH', 'SECOND YEAR Drawing basic building Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.', 0002);

INSERT INTO sessions (course, days, class_time)
VALUES (1, 'M/W/F', '9:00am'),
      (1, 'T/Th', '10:30am'),
      (2, 'M/W', '3:00pm'),
      (2, 'T', '6:00pm'),
      (3, 'M/W/F', '8:15am'),
      (3, 'T/Th', '1:30pm');
