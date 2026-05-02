CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    max_length INTEGER,
    allowed_characters INTEGER,
    use_all INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    seed TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    content TEXT,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    pinned INTEGER
);
