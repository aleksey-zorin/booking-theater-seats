-- ============================================
-- Система бронирования мест в театре: схема БД
-- ============================================

CREATE TABLE IF NOT EXISTS plays (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    duration_min INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY,
    play_id INTEGER NOT NULL,
    datetime TEXT NOT NULL,
    hall TEXT NOT NULL,
    rows INTEGER NOT NULL,
    seats_per_row INTEGER NOT NULL,
    FOREIGN KEY (play_id) REFERENCES plays(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    show_id INTEGER NOT NULL,
    row INTEGER NOT NULL,
    seat INTEGER NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES shows(id)
);
