-- Mock Data For Tests

INSERT INTO users (id, email, password, name, role, major)
VALUES ('89563', 'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$uGAR1DGg$093c0295e6236f7a69b50b283adf1e167cf0c9f92bf965d9127222e16eff18ea', 'teach', 'teacher', 'CSET'),
       ('43784', 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$gIBqHMMV$36e0b5472a8a74fc632f9a85468b201f887e67dd91898b5fbef53c8e4e9981e8', 'studant', 'student', 'CSET');

