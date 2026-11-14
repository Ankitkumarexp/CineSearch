
"""
CineSearch - Student 2
Database Transactions and ACID Properties
Database: SQLite
"""

import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cinesearch.db")


def demonstrate_atomicity(conn):
    """Demonstrate COMMIT and ROLLBACK."""

    cursor = conn.cursor()

    print("\n=== ATOMICITY: COMMIT AND ROLLBACK ===")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction_demo (
            transaction_id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        );
    """)

    conn.commit()

    # Successful transaction
    try:
        cursor.execute("BEGIN TRANSACTION;")

        cursor.execute("""
            INSERT INTO transaction_demo
            (description, amount)
            VALUES (?, ?);
        """, ("Successful transaction", 1000))

        conn.commit()
        print("COMMIT successful.")

    except sqlite3.Error as error:
        conn.rollback()
        print("Transaction rolled back:", error)

    # Failed transaction demonstration
    try:
        cursor.execute("BEGIN TRANSACTION;")

        cursor.execute("""
            INSERT INTO transaction_demo
            (description, amount)
            VALUES (?, ?);
        """, ("Transaction to rollback", 500))

        # Simulate a failure
        raise RuntimeError("Simulated transaction failure")

    except Exception as error:
        conn.rollback()
        print("ROLLBACK executed:", error)

    cursor.execute("""
        SELECT * FROM transaction_demo;
    """)

    print("Records after transactions:")

    for row in cursor.fetchall():
        print(row)


def demonstrate_consistency(conn):
    """Demonstrate data integrity constraints."""

    cursor = conn.cursor()

    print("\n=== CONSISTENCY ===")

    try:
        cursor.execute("BEGIN TRANSACTION;")

        cursor.execute("""
            INSERT INTO rating
            (user_id, movie_id, rating, timestamp)
            VALUES (?, ?, ?, ?);
        """, (999999999, 1, 10.0, 1700000000))

        conn.commit()

    except sqlite3.IntegrityError as error:
        conn.rollback()
        print("Invalid data rejected:", error)

    print("Database constraints protect valid data.")


def demonstrate_isolation(conn):
    """Demonstrate transaction isolation using SQLite."""

    cursor = conn.cursor()

    print("\n=== ISOLATION ===")

    cursor.execute("PRAGMA read_uncommitted;")

    print(
        "Read uncommitted setting:",
        cursor.fetchone()[0]
    )

    print(
        "SQLite transactions isolate uncommitted "
        "changes from other connections by default."
    )


def demonstrate_durability(conn):
    """Demonstrate committed data persistence."""

    cursor = conn.cursor()

    print("\n=== DURABILITY ===")

    cursor.execute("""
        SELECT COUNT(*)
        FROM transaction_demo
        WHERE description = 'Successful transaction';
    """)

    count = cursor.fetchone()[0]

    print("Committed records stored:", count)
    print("Committed changes persist in the database.")


def main():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Run schema and ETL first."
        )

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        demonstrate_atomicity(conn)
        demonstrate_consistency(conn)
        demonstrate_isolation(conn)
        demonstrate_durability(conn)

        print("\nACID demonstration completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
