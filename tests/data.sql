-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$XzIZpgdA$e0c3c01b82c8fb9d633ad9210f51288ccda8dbab9f3600ed8d619531a2d2c4a8', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$bDqUOO42$7ffb03d526f2e00ff5c15d62bfb31ce0f2fecb7158b8fb1fb55c215ba9eb2669', 'student');
