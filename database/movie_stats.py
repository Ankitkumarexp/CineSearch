
"""
CineSearch - Student 2
Movie Statistics and Precomputed Aggregation
Database: SQLite
"""

import os
import sqlite3
import time
import statistics


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


def build_movie_stats(conn):
    """Calculate and store precomputed movie statistics."""

    cursor = conn.cursor()

    print("\n=== BUILDING MOVIE_STATS TABLE ===")

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_stats (
            movie_id INTEGER PRIMARY KEY,
            rating_count INTEGER NOT NULL DEFAULT 0,
            average_rating REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (movie_id)
                REFERENCES movie(movie_id)
                ON DELETE CASCADE
        );
    """)

    conn.commit()

    # Rebuild statistics
    cursor.execute("DELETE FROM movie_stats;")

    start = time.perf_counter()

    cursor.execute("""
        INSERT INTO movie_stats
            (movie_id, rating_count, average_rating)
        SELECT
            m.movie_id,
            COUNT(r.rating_id),
            COALESCE(AVG(r.rating), 0)
        FROM movie m
        LEFT JOIN rating r
            ON m.movie_id = r.movie_id
        GROUP BY m.movie_id;
    """)

    conn.commit()

    calculation_time = time.perf_counter() - start

    print(f"Calculation time: {calculation_time:.4f} seconds")

    cursor.execute("SELECT COUNT(*) FROM movie_stats;")

    print(
        "Total movie statistics records:",
        cursor.fetchone()[0]
    )

    print("\n=== TOP 10 MOVIES BY RATING COUNT ===")

    cursor.execute("""
        SELECT
            m.title,
            ms.rating_count,
            ROUND(ms.average_rating, 2)
        FROM movie_stats ms
        JOIN movie m ON ms.movie_id = m.movie_id
        ORDER BY ms.rating_count DESC
        LIMIT 10;
    """)

    for row in cursor.fetchall():
        print(row)


def benchmark(cursor, query, runs=10):
    """Measure average execution time and standard deviation."""

    cursor.execute(query)
    results = cursor.fetchall()  # Warm-up

    execution_times = []

    for _ in range(runs):
        start = time.perf_counter()

        cursor.execute(query)
        results = cursor.fetchall()

        end = time.perf_counter()

        execution_times.append((end - start) * 1000)

    return (
        statistics.mean(execution_times),
        statistics.stdev(execution_times),
        results
    )


def compare_aggregations(conn):
    """Compare equivalent live and precomputed aggregations."""

    cursor = conn.cursor()

    live_query = """
        SELECT
            m.movie_id,
            COUNT(r.rating_id),
            COALESCE(AVG(r.rating), 0)
        FROM movie m
        LEFT JOIN rating r
            ON m.movie_id = r.movie_id
        GROUP BY m.movie_id;
    """

    precomputed_query = """
        SELECT movie_id, rating_count, average_rating
        FROM movie_stats;
    """

    print("\n=== LIVE VS PRECOMPUTED AGGREGATION ===")

    live_time, live_std, live_data = benchmark(
        cursor, live_query
    )

    pre_time, pre_std, pre_data = benchmark(
        cursor, precomputed_query
    )

    print("\nLive aggregation:")
    print(f"Average time: {live_time:.4f} ms")
    print(f"Standard deviation: {live_std:.4f} ms")

    print("\nPrecomputed aggregation:")
    print(f"Average time: {pre_time:.4f} ms")
    print(f"Standard deviation: {pre_std:.4f} ms")

    # Verify equivalent results
    live_map = {
        row[0]: (row[1], row[2])
        for row in live_data
    }

    pre_map = {
        row[0]: (row[1], row[2])
        for row in pre_data
    }

    mismatches = []

    for movie_id, (live_count, live_avg) in live_map.items():

        pre_count, pre_avg = pre_map.get(
            movie_id, (None, None)
        )

        if (
            pre_count != live_count
            or pre_avg is None
            or abs(live_avg - pre_avg) > 1e-9
        ):
            mismatches.append(movie_id)

    print("\n=== RESULT VERIFICATION ===")
    print("Live records:", len(live_data))
    print("Precomputed records:", len(pre_data))
    print("Mismatched records:", len(mismatches))

    print("\n=== PERFORMANCE COMPARISON ===")

    print(f"Live: {live_time:.4f} ms")
    print(f"Precomputed: {pre_time:.4f} ms")

    if pre_time > 0 and live_time > 0:
        print(f"Speedup: {live_time / pre_time:.2f}x")

        improvement = (
            (live_time - pre_time) / live_time
        ) * 100

        print(f"Time reduction: {improvement:.2f}%")


def main():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema and ETL first."
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        build_movie_stats(conn)
        compare_aggregations(conn)

        print("\nMovie statistics experiments completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
