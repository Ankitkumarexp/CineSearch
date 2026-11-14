
"""
CineSearch - Student 2
SQL Query Library
Database: SQLite
"""

import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


def execute_query(cursor, title, sql, params=()):
    print(f"\n=== {title} ===")
    cursor.execute(sql, params)

    for row in cursor.fetchall():
        print(row)


def main():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema.sql and import_data.py first."
        )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:

        # 1. User Rating History
        execute_query(
            cursor,
            "1. USER RATING HISTORY",
            """
            SELECT u.user_id, m.title, r.rating, r.timestamp
            FROM app_user u
            JOIN rating r ON u.user_id = r.user_id
            JOIN movie m ON r.movie_id = m.movie_id
            WHERE u.user_id = (
                SELECT user_id FROM rating LIMIT 1
            )
            ORDER BY r.timestamp DESC
            LIMIT 10;
            """
        )

        # 2. Ratings for a Movie
        execute_query(
            cursor,
            "2. RATINGS FOR A MOVIE",
            """
            SELECT m.title, r.user_id, r.rating
            FROM movie m
            JOIN rating r ON m.movie_id = r.movie_id
            WHERE m.movie_id = 1
            LIMIT 10;
            """
        )

        # 3. Movie Rating Statistics
        execute_query(
            cursor,
            "3. MOVIE RATING STATISTICS",
            """
            SELECT m.movie_id, m.title,
                   COUNT(r.rating_id) AS rating_count,
                   ROUND(AVG(r.rating), 2) AS average_rating
            FROM movie m
            LEFT JOIN rating r ON m.movie_id = r.movie_id
            GROUP BY m.movie_id, m.title
            ORDER BY rating_count DESC
            LIMIT 10;
            """
        )

        # 4. Popular and Highly Rated Movies
        execute_query(
            cursor,
            "4. POPULAR AND HIGHLY RATED MOVIES",
            """
            SELECT m.title,
                   COUNT(r.rating_id) AS rating_count,
                   ROUND(AVG(r.rating), 2) AS average_rating
            FROM movie m
            JOIN rating r ON m.movie_id = r.movie_id
            GROUP BY m.movie_id, m.title
            HAVING COUNT(r.rating_id) >= 20
            ORDER BY average_rating DESC, rating_count DESC
            LIMIT 10;
            """
        )

        # 5. Genre-Based Movie Filtering
        execute_query(
            cursor,
            "5. GENRE-BASED MOVIE FILTERING",
            """
            SELECT m.title, g.genre_name
            FROM movie m
            JOIN movie_genre mg ON m.movie_id = mg.movie_id
            JOIN genre g ON mg.genre_id = g.genre_id
            WHERE g.genre_name = 'Action'
            LIMIT 10;
            """
        )

        # 6. Genre-Wise Rating Statistics
        execute_query(
            cursor,
            "6. GENRE-WISE RATING STATISTICS",
            """
            SELECT g.genre_name,
                   COUNT(r.rating_id) AS rating_count,
                   ROUND(AVG(r.rating), 2) AS average_rating
            FROM genre g
            JOIN movie_genre mg ON g.genre_id = mg.genre_id
            JOIN rating r ON mg.movie_id = r.movie_id
            GROUP BY g.genre_id, g.genre_name
            ORDER BY average_rating DESC;
            """
        )

        # 7. Popular Tags
        execute_query(
            cursor,
            "7. POPULAR TAGS",
            """
            SELECT tag_text, COUNT(*) AS tag_count
            FROM tag_event
            GROUP BY tag_text
            ORDER BY tag_count DESC
            LIMIT 10;
            """
        )

        print("\nSQL Query Library Completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
