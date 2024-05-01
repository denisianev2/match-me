
INSERT INTO users (email, password_hash, type) VALUES
('denis@ianev.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentee'),
('mentor1@email.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentor'),
('mentor2@email.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentor'),
('mentor3@email.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentor'),
('mentee1@email.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentee'),
('mentee2@email.com', '$argon2i$v=19$m=16,t=2,p=1$RW5Xb09JaExuVW8zTkNEMw$5QqpRnFkUkCNf1NdiKy0iA', 'mentee');

INSERT INTO roles (name) VALUES
('Sales'),
('Tech');

INSERT INTO cities (name) VALUES
('London'),
('Manchester'),
('Birmingham'),
('Glasgow'),
('Leeds'),
('Liverpool'),
('Newcastle'),
('Sheffield'),
('Bristol'),
('Edinburgh');

INSERT INTO "countries" ("name") VALUES ('UK');

INSERT INTO "theatres" ("name") VALUES
('APJC'),
('EMEAR'),
('AMER');

INSERT INTO strengths (name) VALUES
('Leadership'),
('Communication'),
('Problem-solving'),
('Creativity'),
('Adaptability'),
('Teamwork'),
('Time management'),
('Critical thinking'),
('Organization'),
('Decision-making');

INSERT INTO "interests" ("name") VALUES
('Music'),
('Sports'),
('Reading'),
('Cooking'),
('Traveling'),
('Photography'),
('Gaming'),
('Art'),
('Fashion'),
('Fitness');

INSERT INTO titles (name) VALUES
('Network Engineer'),
('Systems Engineer'),
('Security Engineer'),
('Collaboration Engineer'),
('Data Center Engineer'),
('Wireless Engineer'),
('Cloud Engineer'),
('DevOps Engineer');

INSERT INTO "profiles" (
  "user_id",
  "role_id",
  "title_id",
  "gender",
  "city_id",
  "country_id",
  "theatre_id",
  "bio",
  "csap_track",
  "same_theatre",
  "same_gender",
  "same_role",
  "first_priority",
  "second_priority"
)

VALUES
(1, 2, 1, 'male', 1, 1, 1, 'I am Denis', 'engineer', 'no_preference', 'no_preference', 'no_preference', 'strengths', 'none'),
(2, 2, 2, 'male', 1, 1, 1, 'I am Mentor 1', 'sales', 'no_preference', 'no_preference', 'no_preference', 'strengths', 'none'),
(3, 2, 3, 'female', 1, 1, 1, 'I am Mentor 2', 'engineer', 'no_preference', 'no_preference', 'no_preference', 'strengths', 'none'),
(4, 1, 4, 'male', 1, 1, 1, 'I am Mentor 3', 'sales', 'no_preference', 'no_preference', 'no_preference', 'strengths', 'none'),
(5, 1, 5, 'female', 1, 1, 1, 'I am Mentee 1', 'sales', 'no_preference', 'no_preference', 'no_preference', 'strengths', 'none');