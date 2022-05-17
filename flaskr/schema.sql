DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS kentiku;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE kentiku (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    kentiku_name TEXT,
    name_of_creater TEXT,
    location_addr TEXT,
    year_month_founded TEXT,
    memo TEXT
    img TEXT
);