
-- CineSearch: Student 2
-- Database Schema
-- DBMS: SQLite

PRAGMA foreign_keys = ON;

-- 1. Movie Table
CREATE TABLE IF NOT EXISTS movie (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INTEGER,
    imdb_id INTEGER,
    tmdb_id INTEGER
);

-- 2. Genre Table
CREATE TABLE IF NOT EXISTS genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT NOT NULL UNIQUE
);

-- 3. Movie Genre Junction Table
CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
        ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
        ON DELETE CASCADE
);

-- 4. App User Table
CREATE TABLE IF NOT EXISTS app_user (
    user_id INTEGER PRIMARY KEY
);

-- 5. Rating Table
CREATE TABLE IF NOT EXISTS rating (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL
        CHECK(rating >= 0.5 AND rating <= 5.0),
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES app_user(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
        ON DELETE CASCADE,
    UNIQUE(user_id, movie_id)
);

-- 6. Tag Event Table
CREATE TABLE IF NOT EXISTS tag_event (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    tag_text TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES app_user(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
        ON DELETE CASCADE
);

-- 7. Movie Statistics Table
CREATE TABLE IF NOT EXISTS movie_stats (
    movie_id INTEGER PRIMARY KEY,
    rating_count INTEGER NOT NULL DEFAULT 0
        CHECK(rating_count >= 0),
    average_rating REAL NOT NULL DEFAULT 0
        CHECK(average_rating >= 0 AND average_rating <= 5.0),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
        ON DELETE CASCADE
);
