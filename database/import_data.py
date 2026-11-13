
"""
CineSearch - Student 2
MovieLens ETL Pipeline
Database: SQLite
"""

import os
import re
import sqlite3
import pandas as pd

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data", "ml-32m")
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")

CHUNK_SIZE = 200_000
RATING_SAMPLE_DIVISOR = 32


def extract_year(title):
    """Extract release year from movie title."""

    match = re.search(r'\((\d{4})\)\s*$', title)

    if match:
        year = int(match.group(1))
        clean_title = re.sub(
            r'\s*\(\d{4}\)\s*$',
            '',
            title
        ).strip()

        return year, clean_title

    return None, title.strip()


def import_movies(conn):
    """Import movies, genres and external links."""

    print("\nLoading movies dataset...")

    movies_path = os.path.join(DATA_DIR, "movies.csv")
    links_path = os.path.join(DATA_DIR, "links.csv")

    movies_df = pd.read_csv(movies_path)
    links_df = pd.read_csv(links_path)

    all_genres = set()

    for genres in movies_df["genres"].dropna():
        if genres != "(no genres listed)":
            all_genres.update(genres.split("|"))

    cursor = conn.cursor()

    with conn:
        cursor.executemany(
            "INSERT OR IGNORE INTO genre (genre_name) VALUES (?);",
            [(genre,) for genre in sorted(all_genres)]
        )

        cursor.execute(
            "SELECT genre_id, genre_name FROM genre;"
        )

        genre_map = {
            name: genre_id
            for genre_id, name in cursor.fetchall()
        }

        links_map = {}

        for row in links_df.itertuples(index=False):
            movie_id = int(row.movieId)

            imdb_id = (
                int(row.imdbId)
                if pd.notna(row.imdbId) else None
            )

            tmdb_id = (
                int(row.tmdbId)
                if pd.notna(row.tmdbId) else None
            )

            links_map[movie_id] = (imdb_id, tmdb_id)

        movie_records = []
        movie_genre_records = []

        for row in movies_df.itertuples(index=False):

            movie_id = int(row.movieId)
            year, clean_title = extract_year(str(row.title))

            imdb_id, tmdb_id = links_map.get(
                movie_id, (None, None)
            )

            movie_records.append(
                (movie_id, clean_title, year, imdb_id, tmdb_id)
            )

            if (
                pd.notna(row.genres)
                and row.genres != "(no genres listed)"
            ):
                for genre in row.genres.split("|"):

                    if genre in genre_map:
                        movie_genre_records.append(
                            (movie_id, genre_map[genre])
                        )

        cursor.executemany("""
            INSERT OR IGNORE INTO movie
            (movie_id, title, release_year, imdb_id, tmdb_id)
            VALUES (?, ?, ?, ?, ?);
        """, movie_records)

        cursor.executemany("""
            INSERT OR IGNORE INTO movie_genre
            (movie_id, genre_id)
            VALUES (?, ?);
        """, movie_genre_records)

    print("Movies imported:", len(movie_records))
    print("Genres processed:", len(genre_map))
    print("Movie-genre relationships:", len(movie_genre_records))


def import_ratings(conn):
    """Import reproducible Stage 1 ratings subset."""

    print("\nImporting ratings in chunks...")

    ratings_path = os.path.join(DATA_DIR, "ratings.csv")

    inserted_users = set()
    inserted_count = 0
    skipped_count = 0

    cursor = conn.cursor()

    for chunk in pd.read_csv(
        ratings_path,
        chunksize=CHUNK_SIZE
    ):

        subset = chunk[
            chunk["userId"] % RATING_SAMPLE_DIVISOR == 0
        ]

        if subset.empty:
            continue

        users = set(subset["userId"].unique())
        new_users = users - inserted_users

        rating_records = [
            (
                int(row.userId),
                int(row.movieId),
                float(row.rating),
                int(row.timestamp)
            )
            for row in subset.itertuples(index=False)
        ]

        with conn:

            cursor.executemany(
                """
                INSERT OR IGNORE INTO app_user (user_id)
                VALUES (?);
                """,
                [(int(uid),) for uid in new_users]
            )

            changes_before = conn.total_changes

            cursor.executemany("""
                INSERT OR IGNORE INTO rating
                (user_id, movie_id, rating, timestamp)
                VALUES (?, ?, ?, ?);
            """, rating_records)

            inserted_in_chunk = (
                conn.total_changes - changes_before
            )

        inserted_count += inserted_in_chunk
        skipped_count += len(subset) - inserted_in_chunk

        inserted_users.update(users)

    print("Users processed:", len(inserted_users))
    print("New ratings inserted:", inserted_count)
    print("Ratings ignored:", skipped_count)


def import_tags(conn):
    """Import valid tag events using chunked processing."""

    print("\nImporting tags...")

    tags_path = os.path.join(DATA_DIR, "tags.csv")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM app_user")
    valid_users = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT movie_id FROM movie")
    valid_movies = {row[0] for row in cursor.fetchall()}

    inserted_tags = 0
    skipped_tags = 0

    # Clear previous imported tags to avoid duplicates on reruns.
    with conn:
        cursor.execute("DELETE FROM tag_event")

    for chunk in pd.read_csv(
        tags_path,
        chunksize=CHUNK_SIZE
    ):

        chunk["tag"] = (
            chunk["tag"].astype("string").str.strip()
        )

        subset = chunk[
            chunk["userId"].isin(valid_users)
            & chunk["movieId"].isin(valid_movies)
            & chunk["tag"].notna()
            & (chunk["tag"] != "")
        ]

        skipped_tags += len(chunk) - len(subset)

        if subset.empty:
            continue

        tag_records = [
            (
                int(row.userId),
                int(row.movieId),
                str(row.tag),
                int(row.timestamp)
            )
            for row in subset.itertuples(index=False)
        ]

        with conn:
            cursor.executemany("""
                INSERT INTO tag_event
                (user_id, movie_id, tag_text, timestamp)
                VALUES (?, ?, ?, ?);
            """, tag_records)

        inserted_tags += len(tag_records)

    print("Tags inserted:", inserted_tags)
    print("Invalid tags skipped:", skipped_tags)


def verify_database(conn):
    """Verify imported data and foreign-key integrity."""

    cursor = conn.cursor()

    print("\nDatabase verification:")

    tables = [
        "movie",
        "genre",
        "movie_genre",
        "app_user",
        "rating",
        "tag_event",
        "movie_stats"
    ]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]:,}")

    cursor.execute("PRAGMA foreign_key_check")
    violations = cursor.fetchall()

    print("Foreign key violations:", violations)


def main():

    required_files = [
        "movies.csv",
        "ratings.csv",
        "tags.csv",
        "links.csv"
    ]

    for filename in required_files:
        path = os.path.join(DATA_DIR, filename)

        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Dataset file not found: {path}"
            )

    if not os.path.isfile(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema.sql first."
        )

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        import_movies(conn)
        import_ratings(conn)
        import_tags(conn)
        verify_database(conn)

        print("\nETL pipeline completed successfully!")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
