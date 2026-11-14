
"""
CineSearch - Student 2
Database Scalability and Storage Analysis
Database: SQLite
"""

import os
import sqlite3
import time
import statistics


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


def get_database_size():
    """Calculate total database file size."""

    size_bytes = os.path.getsize(DB_PATH)

    print("\n=== DATABASE STORAGE ===")
    print(f"Database size: {size_bytes / (1024 * 1024):.2f} MB")
    print(f"Database size: {size_bytes:,} bytes")


def analyze_table_sizes(cursor):
    """Display row counts for database tables."""

    print("\n=== TABLE SCALABILITY ===")

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
        count = cursor.fetchone()[0]

        print(f"{table}: {count:,} records")


def analyze_index_storage(cursor):
    """Estimate index storage using SQLite DBSTAT."""

    print("\n=== INDEX STORAGE ANALYSIS ===")

    try:
        cursor.execute("""
            SELECT
                name,
                SUM(pgsize) AS total_bytes
            FROM dbstat
            WHERE name IN (
                SELECT name
                FROM sqlite_master
                WHERE type = 'index'
            )
            GROUP BY name
            ORDER BY total_bytes DESC;
        """)

        results = cursor.fetchall()

        if not results:
            print("No indexes found.")
            return

        for name, size in results:
            print(
                f"{name}: {size:,} bytes "
                f"({size / 1024:.2f} KB)"
            )

    except sqlite3.OperationalError:
        print("SQLite DBSTAT is unavailable.")
        print("Index storage details cannot be measured.")


def benchmark_query(cursor, query, params, runs=10):
    """Measure average execution time."""

    cursor.execute(query, params)
    cursor.fetchall()

    times = []

    for _ in range(runs):
        start = time.perf_counter()

        cursor.execute(query, params)
        cursor.fetchall()

        end = time.perf_counter()

        times.append((end - start) * 1000)

    return statistics.mean(times)


def scalability_experiment(cursor):
    """Compare query response time across rating subsets."""

    print("\n=== SCALABILITY EXPERIMENT ===")

    cursor.execute("SELECT COUNT(*) FROM rating")
    total_records = cursor.fetchone()[0]

    if total_records == 0:
        print("Rating table is empty.")
        return

    cursor.execute("""
        SELECT MIN(rating_id), MAX(rating_id)
        FROM rating
    """)

    min_id, max_id = cursor.fetchone()

    if min_id is None:
        return

    query = """
        SELECT COUNT(*), AVG(rating)
        FROM rating
        WHERE rating_id <= ?
    """

    percentages = [10, 25, 50, 75, 100]

    for percentage in percentages:

        target_records = max(
            1,
            int(total_records * percentage / 100)
        )

        cursor.execute("""
            SELECT rating_id
            FROM rating
            ORDER BY rating_id
            LIMIT 1 OFFSET ?
        """, (target_records - 1,))

        row = cursor.fetchone()

        if row is None:
            continue

        threshold = row[0]

        avg_time = benchmark_query(
            cursor,
            query,
            (threshold,)
        )

        print(
            f"{percentage}% data "
            f"({target_records:,} records): "
            f"{avg_time:.4f} ms"
        )


def analyze_database_indexes(cursor):
    """List all database indexes."""

    print("\n=== DATABASE INDEX INVENTORY ===")

    cursor.execute("""
        SELECT name, tbl_name
        FROM sqlite_master
        WHERE type = 'index'
        AND name NOT LIKE 'sqlite_autoindex%'
        ORDER BY tbl_name, name;
    """)

    indexes = cursor.fetchall()

    if not indexes:
        print("No secondary indexes found.")
        return

    for name, table in indexes:
        print(f"Index: {name} | Table: {table}")


def query_plan_analysis(cursor):
    """Inspect the execution plan of a rating lookup."""

    print("\n=== SCALABILITY QUERY PLAN ===")

    query = """
        SELECT *
        FROM rating
        WHERE user_id = 320;
    """

    cursor.execute(
        "EXPLAIN QUERY PLAN " + query
    )

    for row in cursor.fetchall():
        print(row)


def main():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema and ETL first."
        )

    # Read-only connection protects existing data.
    conn = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )

    try:
        cursor = conn.cursor()

        get_database_size()
        analyze_table_sizes(cursor)
        analyze_index_storage(cursor)
        analyze_database_indexes(cursor)
        scalability_experiment(cursor)
        query_plan_analysis(cursor)

        print("\nScalability analysis completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
