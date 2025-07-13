CREATE TABLE users (
    id INTEGER,
    username TEXT NOT NULL,
    profile_pic_id INTEGER CHECK(profile_pic_id >= 1 AND profile_pic_id <= 8) DEFAULT 6 NOT NULL,
    streak INTEGER NOT NULL DEFAULT 0 CHECK(streak >= 0),
    hash TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE decks (
    id INTEGER,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    color TEXT NOT NULL CHECK(color IN ('red', 'yellow', 'blue', 'green')),
    icon INTEGER NOT NULL CHECK(icon >= 1 AND icon <= 6),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cards (
    id INTEGER,
    deck_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(deck_id) REFERENCES decks(id) ON DELETE CASCADE
);

CREATE TABLE progresses (
    id INTEGER,
    card_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    progress INTEGER DEFAULT 0 NOT NULL CHECK(progress >= 0 AND progress <= 10),
    PRIMARY KEY(id),
    FOREIGN KEY(card_id) REFERENCES cards(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE sessions (
    id INTEGER,
    user_id INTEGER NOT NULL,
    log_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX username ON users(username);
CREATE INDEX deck ON decks(user_id, name);
CREATE INDEX cards_in_deck ON cards(deck_id);
CREATE UNIQUE INDEX unique_deck_name_per_user ON decks(user_id, name);

CREATE TRIGGER insert_progress_after_card
AFTER INSERT ON cards
BEGIN
    INSERT INTO progresses (card_id, user_id)
    SELECT NEW.id, decks.user_id
    FROM decks
    WHERE decks.id = NEW.deck_id;
END;
