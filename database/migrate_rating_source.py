
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "cinesearch.db"

conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("BEGIN")

    columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(rating)")
    }

    if "rating_source" not in columns:
        conn.execute("""
            ALTER TABLE rating
            ADD COLUMN rating_source TEXT NOT NULL
            DEFAULT 'movielens'
            CHECK(rating_source IN ('movielens', 'community'))
        """)

    # Classify the five existing CineSearch ratings.
    cursor = conn.execute("""
        UPDATE rating
        SET rating_source = 'community'
        WHERE user_id = 999999
    """)

    if cursor.rowcount != 5:
        raise RuntimeError(
            f"Expected 5 personal ratings, found {cursor.rowcount}"
        )

    # Preserve and classify the extra legacy Toy Story rating.
    cursor = conn.execute("""
        UPDATE rating
        SET rating_source = 'community'
        WHERE user_id = 101
          AND movie_id = 1
          AND rating = 5.0
          AND timestamp = 1794657695
    """)

    if cursor.rowcount != 1:
        raise RuntimeError(
            "Expected exactly one legacy Toy Story rating"
        )

    conn.commit()

    print("Rating-source migration completed.")

    print("\nRating-source counts:")
    for row in conn.execute("""
        SELECT rating_source, COUNT(*)
        FROM rating
        GROUP BY rating_source
    """):
        print(row)

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
