-- PostgreSQL-compatible logical schema
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(180) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL,
  skills JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE courses (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  trainer_id INTEGER REFERENCES users(id),
  skill_tag VARCHAR(100) NOT NULL,
  resource_url TEXT
);

CREATE TABLE enrollments (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  course_id INTEGER REFERENCES courses(id),
  progress INTEGER DEFAULT 0,
  status VARCHAR(30) DEFAULT 'enrolled'
);

CREATE TABLE quizzes (
  id SERIAL PRIMARY KEY,
  course_id INTEGER REFERENCES courses(id),
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  answer VARCHAR(255) NOT NULL
);

CREATE TABLE results (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  quiz_id INTEGER REFERENCES quizzes(id),
  score NUMERIC(5,2),
  weak_skill VARCHAR(100)
);

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  course_id INTEGER REFERENCES courses(id),
  certificate_id VARCHAR(100),
  status VARCHAR(30)
);
