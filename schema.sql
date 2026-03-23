CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE games (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  seed_length INTEGER,
  seed_allowed TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    seed TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games
);
