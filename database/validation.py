
"""
CineSearch - Student 2
Database Validation and Integrity Checks
Database: SQLite
"""

import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


REQUIRED_TABLES = [
    "movie",
    "genre",
    "movie_genre",
    "app_user",
    "rating",
    "tag_event",
    "movie_stats"
]


def check_tables(cursor):
    """Check whether all required tables exist."""

    print("\n=== TABLE VALIDATION ===")

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table';
    """)

    existing = {row[0] for row in cursor.fetchall()}

    for table in REQUIRED_TABLES:
        status = "PASS" if table in existing else "FAIL"
        print(f"{table}: {status}")

    return all(table in existing for table in REQUIRED_TABLES)


def check_record_counts(cursor):
    """Display records in all major tables."""

    print("\n=== RECORD COUNT VALIDATION ===")

    for table in REQUIRED_TABLES:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        print(f"{table}: {count:,} records")


def check_foreign_keys(cursor):
    """Check foreign key violations."""

    print("\n=== FOREIGN KEY VALIDATION ===")

    cursor.execute("PRAGMA foreign_key_check;")
    violations = cursor.fetchall()

    if violations:
        print("FAIL: Foreign key violations found.")

        for violation in violations:
            print(violation)

        return False

    print("PASS: No foreign key violations.")
    return True


def check_rating_values(cursor):
    """Check rating values are within the valid range."""

    print("\n=== RATING VALIDATION ===")

    cursor.execute("""
        SELECT COUNT(*)
        FROM rating
        WHERE rating < 0.5 OR rating > 5.0;
    """)

    invalid = cursor.fetchone()[0]

    if invalid == 0:
        print("PASS: All ratings are between 0.5 and 5.0.")
        return True

    print("FAIL: Invalid ratings found:", invalid)
    return False


def check_duplicate_ratings(cursor):
    """Check duplicate user-movie rating combinations."""

    print("\n=== DUPLICATE RATING VALIDATION ===")

    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT user_id, movie_id
            FROM rating
            GROUP BY user_id, movie_id
            HAVING COUNT(*) > 1
        );
    """)

    duplicates = cursor.fetchone()[0]

    if duplicates == 0:
        print("PASS: No duplicate user-movie ratings.")
        return True

    print("FAIL: Duplicate combinations found:", duplicates)
    return False


def check_movie_genre_relationships(cursor):
    """Check movie-genre relationship integrity."""

    print("\n=== MOVIE-GENRE VALIDATION ===")

    cursor.execute("""
        SELECT COUNT(*)
        FROM movie_genre mg
        LEFT JOIN movie m
            ON mg.movie_id = m.movie_id
        LEFT JOIN genre g
            ON mg.genre_id = g.genre_id
        WHERE m.movie_id IS NULL
           OR g.genre_id IS NULL;
    """)

    invalid = cursor.fetchone()[0]

    if invalid == 0:
        print("PASS: All movie-genre references are valid.")
        return True

    print("FAIL: Invalid relationships:", invalid)
    return False


def check_null_values(cursor):
    """Check important columns for unexpected NULL values."""

    print("\n=== NULL VALUE VALIDATION ===")

    checks = {
        "movie": ["movie_id", "title"],
        "genre": ["genre_id", "genre_name"],
        "rating": ["user_id", "movie_id", "rating"],
        "tag_event": ["user_id", "movie_id", "tag_text"]
    }

    passed = True

    for table, columns in checks.items():

        for column in columns:

            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE {column} IS NULL;
            """)

            count = cursor.fetchone()[0]

            status = "PASS" if count == 0 else "FAIL"

            print(f"{table}.{column}: {status} ({count})")

            if count > 0:
                passed = False

    return passed


def main():

    if not os.path.isfile(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema and ETL first."
        )

    conn = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )

    try:
        cursor = conn.cursor()

        print("=" * 45)
        print("CINESEARCH DATABASE VALIDATION")
        print("=" * 45)

        tables_ok = check_tables(cursor)

        if not tables_ok:
            print("\nValidation stopped: Required tables missing.")
            return

        check_record_counts(cursor)

        results = [
            check_foreign_keys(cursor),
            check_rating_values(cursor),
            check_duplicate_ratings(cursor),
            check_movie_genre_relationships(cursor),
            check_null_values(cursor)
        ]

        print("\n=== FINAL VALIDATION RESULT ===")

        if all(results):
            print("ALL DATABASE VALIDATION CHECKS PASSED.")
        else:
            print("SOME DATABASE VALIDATION CHECKS FAILED.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
