
import os
import sqlite3
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "cinesearch.db"

TMDB_API_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

_poster_cache = {}


def get_db_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def initialize_poster_cache():
    """Create persistent poster cache table once."""
    connection = get_db_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS poster_cache (
                movie_id INTEGER PRIMARY KEY,
                poster_url TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
    finally:
        connection.close()


def get_movie_poster(movie_id):
    """Return poster URL using memory, SQLite, or TMDB."""

    # 1. Check in-memory cache.
    if movie_id in _poster_cache:
        return _poster_cache[movie_id]

    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        return None

    # 2. Check SQLite and retrieve TMDB ID
    # using a single database connection.
    connection = get_db_connection()

    try:
        cached_row = connection.execute(
            "SELECT poster_url FROM poster_cache WHERE movie_id = ?",
            (movie_id,)
        ).fetchone()

        if cached_row:
            _poster_cache[movie_id] = cached_row[0]
            return cached_row[0]

        movie_row = connection.execute(
            "SELECT tmdb_id FROM movie WHERE movie_id = ?",
            (movie_id,)
        ).fetchone()

        tmdb_id = movie_row[0] if movie_row else None

    finally:
        connection.close()

    if not tmdb_id:
        return None

    # 3. Request poster from TMDB.
    try:
        response = requests.get(
            f"{TMDB_API_URL}/{tmdb_id}",
            params={"api_key": api_key},
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")

        poster_url = (
            f"{TMDB_IMAGE_BASE}{poster_path}"
            if poster_path else None
        )

        # 4. Save result in persistent SQLite cache.
        connection = get_db_connection()

        try:
            connection.execute("""
                INSERT OR REPLACE INTO poster_cache
                (movie_id, poster_url, cached_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (movie_id, poster_url))

            connection.commit()

        finally:
            connection.close()

        _poster_cache[movie_id] = poster_url

        return poster_url

    except requests.RequestException as error:
        print(
            f"TMDB poster lookup failed for movie "
            f"{movie_id}: {error}"
        )
        return None


# Initialize cache table when the service loads.
initialize_poster_cache()
