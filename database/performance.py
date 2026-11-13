
"""
CineSearch - Student 2
Database Performance and Indexing Experiments
Database: SQLite
"""

import os
import sqlite3
import time
import statistics


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


QUERIES = {
    "User Rating History": """
        SELECT * FROM rating WHERE user_id = 320;
    """,

    "Movie Ratings": """
        SELECT * FROM rating WHERE movie_id = 1;
    """,

    "User-Movie Lookup": """
        SELECT * FROM rating
        WHERE user_id = 320 AND movie_id = 1;
    """,

    "Movie Rating Aggregation": """
        SELECT movie_id, COUNT(*), AVG(rating)
        FROM rating GROUP BY movie_id;
    """,

    "Movie Genre Filtering": """
        SELECT movie_id FROM movie_genre
        WHERE genre_id = 1;
    """,

    "Tag Movie Lookup": """
        SELECT * FROM tag_event WHERE movie_id = 1;
    """
}


INDEX_COMMANDS = [
    "CREATE INDEX IF NOT EXISTS idx_rating_user_id ON rating(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_rating_movie_id ON rating(movie_id);",
    "CREATE INDEX IF NOT EXISTS idx_rating_user_movie ON rating(user_id, movie_id);",
    "CREATE INDEX IF NOT EXISTS idx_movie_genre_genre ON movie_genre(genre_id);",
    "CREATE INDEX IF NOT EXISTS idx_tag_event_movie_id ON tag_event(movie_id);"
]


INDEX_NAMES = [
    "idx_rating_user_id",
    "idx_rating_movie_id",
    "idx_rating_user_movie",
    "idx_movie_genre_genre",
    "idx_tag_event_movie_id"
]


def benchmark(cursor, query, runs=15):
    """Measure average query execution time."""

    cursor.execute(query)
    cursor.fetchall()

    times = []

    for _ in range(runs):
        start = time.perf_counter()

        cursor.execute(query)
        cursor.fetchall()

        end = time.perf_counter()

        times.append((end - start) * 1000)

    return statistics.mean(times), (
        statistics.stdev(times) if len(times) > 1 else 0
    )


def baseline_experiment(cursor):
    """Measure query performance without selected indexes."""

    print("\n=== BASELINE QUERY PERFORMANCE ===")

    results = {}

    for name, query in QUERIES.items():
        avg, std = benchmark(cursor, query, runs=10)
        results[name] = avg

        print(f"{name}: {avg:.4f} ms | SD: {std:.4f} ms")

    return results


def controlled_index_experiment(conn, cursor):
    """Compare query performance before and after indexing."""

    print("\n=== CONTROLLED INDEX EXPERIMENT ===")

    for name in INDEX_NAMES:
        cursor.execute(f"DROP INDEX IF EXISTS {name};")

    conn.commit()

    before = {}

    print("\nPerformance WITHOUT selected indexes:")

    for name, query in QUERIES.items():
        avg, std = benchmark(cursor, query)
        before[name] = avg
        print(f"{name}: {avg:.4f} ms | SD: {std:.4f} ms")

    print("\nCreating indexes...")

    start = time.perf_counter()

    for sql in INDEX_COMMANDS:
        cursor.execute(sql)

    conn.commit()

    print(
        "Index creation time:",
        f"{time.perf_counter() - start:.4f} seconds"
    )

    after = {}

    print("\nPerformance WITH indexes:")

    for name, query in QUERIES.items():
        avg, std = benchmark(cursor, query)
        after[name] = avg
        print(f"{name}: {avg:.4f} ms | SD: {std:.4f} ms")

    print("\n=== BEFORE VS AFTER COMPARISON ===")

    for name in QUERIES:
        old = before[name]
        new = after[name]

        improvement = (
            ((old - new) / old) * 100 if old > 0 else 0
        )

        print(f"\n{name}")
        print(f"Before: {old:.4f} ms")
        print(f"After: {new:.4f} ms")
        print(f"Change: {improvement:.2f}%")

    return before, after


def query_plan_experiment(cursor):
    """Display SQLite query execution plans."""

    print("\n=== EXPLAIN QUERY PLAN ===")

    for name, query in QUERIES.items():
        print(f"\n--- {name} ---")

        cursor.execute("EXPLAIN QUERY PLAN " + query)

        for row in cursor.fetchall():
            print(row)


def composite_index_experiment(conn, cursor):
    """Compare composite index column ordering."""

    print("\n=== COMPOSITE INDEX COLUMN ORDER ===")

    cursor.execute("DROP INDEX IF EXISTS idx_test_user_movie")
    cursor.execute("DROP INDEX IF EXISTS idx_test_movie_user")

    cursor.execute("""
        CREATE INDEX idx_test_user_movie
        ON rating(user_id, movie_id);
    """)

    cursor.execute("""
        CREATE INDEX idx_test_movie_user
        ON rating(movie_id, user_id);
    """)

    conn.commit()

    cursor.execute("""
        SELECT user_id, movie_id FROM rating LIMIT 1;
    """)

    sample = cursor.fetchone()

    if sample is None:
        print("Rating table is empty.")
        return

    user_id, movie_id = sample

    tests = [
        ("User first", "idx_test_user_movie"),
        ("Movie first", "idx_test_movie_user")
    ]

    for label, index_name in tests:

        query = f"""
            SELECT rating FROM rating INDEXED BY {index_name}
            WHERE user_id = ? AND movie_id = ?;
        """

        print(f"\n{label}:")

        cursor.execute(
            "EXPLAIN QUERY PLAN " + query,
            (user_id, movie_id)
        )

        print("Query plan:", cursor.fetchall())

        times = []

        for _ in range(100):
            start = time.perf_counter()

            cursor.execute(query, (user_id, movie_id))
            cursor.fetchall()

            times.append(time.perf_counter() - start)

        print(
            "Average time:",
            f"{statistics.mean(times):.8f} seconds"
        )

    cursor.execute("DROP INDEX IF EXISTS idx_test_user_movie")
    cursor.execute("DROP INDEX IF EXISTS idx_test_movie_user")
    conn.commit()


def insertion_overhead_experiment(conn, cursor):
    """Compare insertion time with and without secondary indexes."""

    print("\n=== INDEX INSERTION OVERHEAD ===")

    cursor.execute("DROP TABLE IF EXISTS rating_insert_no_index")
    cursor.execute("DROP TABLE IF EXISTS rating_insert_with_index")

    for table in ["rating_insert_no_index", "rating_insert_with_index"]:
        cursor.execute(f"""
            CREATE TABLE {table} AS
            SELECT user_id, movie_id, rating, timestamp
            FROM rating WHERE 0;
        """)

    cursor.execute("""
        CREATE INDEX idx_insert_user
        ON rating_insert_with_index(user_id);
    """)

    cursor.execute("""
        CREATE INDEX idx_insert_movie
        ON rating_insert_with_index(movie_id);
    """)

    conn.commit()

    start = time.perf_counter()

    cursor.execute("""
        INSERT INTO rating_insert_no_index
        SELECT user_id, movie_id, rating, timestamp FROM rating;
    """)

    conn.commit()
    no_index_time = time.perf_counter() - start

    start = time.perf_counter()

    cursor.execute("""
        INSERT INTO rating_insert_with_index
        SELECT user_id, movie_id, rating, timestamp FROM rating;
    """)

    conn.commit()
    with_index_time = time.perf_counter() - start

    cursor.execute("SELECT COUNT(*) FROM rating_insert_no_index")
    count = cursor.fetchone()[0]

    print("Rows inserted:", count)
    print(f"Without indexes: {no_index_time:.4f} seconds")
    print(f"With indexes: {with_index_time:.4f} seconds")

    if no_index_time > 0:
        overhead = (
            (with_index_time - no_index_time) / no_index_time
        ) * 100

        print(f"Insertion overhead: {overhead:.2f}%")

    cursor.execute("DROP TABLE rating_insert_no_index")
    cursor.execute("DROP TABLE rating_insert_with_index")

    conn.commit()


def main():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run database setup and ETL first."
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        baseline_experiment(cursor)

        controlled_index_experiment(conn, cursor)

        query_plan_experiment(cursor)

        composite_index_experiment(conn, cursor)

        insertion_overhead_experiment(conn, cursor)

        print("\nAll performance experiments completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
