CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER NOT NULL PRIMARY KEY,
    started BIGINT NOT NULL,
    finished BIGINT NULL DEFAULT NULL
);

/*
    result:
    - 0: draw
    - 1: looser
    - 2: winner
 */
CREATE TABLE IF NOT EXISTS game_users (
    game INTEGER NOT NULL,
    user INTEGER NOT NULL,
    result INTEGER NULL DEFAULT NULL,
    PRIMARY KEY (game, user),
    FOREIGN KEY (game) REFERENCES games (id) ON DELETE CASCADE,
    FOREIGN KEY (user) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER NOT NULL PRIMARY KEY,
    from_user INTEGER NOT NULL,
    to_user INTEGER NULL DEFAULT NULL,
    message TEXT NOT NULL,
    created BIGINT NOT NULL,
    FOREIGN KEY (from_user) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (to_user) REFERENCES users (id) ON DELETE CASCADE
);
