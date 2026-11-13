
import sqlite3
import unittest
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "database" / "schema.sql"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            self.connection.executescript(file.read())

        self.connection.execute(
            "INSERT INTO movie (movie_id, title) VALUES (1, 'Test Movie')"
        )
        self.connection.execute(
            "INSERT INTO app_user (user_id) VALUES (1)"
        )
        self.connection.commit()

    def tearDown(self):
        self.connection.close()

    def test_required_tables_exist(self):
        tables = {
            row[0] for row in self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        expected = {
            "movie", "genre", "movie_genre",
            "app_user", "rating", "tag_event", "movie_stats"
        }

        self.assertTrue(expected.issubset(tables))

    def test_invalid_rating_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("""
                INSERT INTO rating (user_id, movie_id, rating, timestamp)
                VALUES (1, 1, 6.0, 1000)
            """)

    def test_foreign_key_enforcement(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("""
                INSERT INTO rating (user_id, movie_id, rating, timestamp)
                VALUES (999, 999, 4.0, 1000)
            """)

    def test_genre_uniqueness(self):
        self.connection.execute(
            "INSERT INTO genre (genre_name) VALUES ('Action')"
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO genre (genre_name) VALUES ('Action')"
            )


if __name__ == "__main__":
    unittest.main()
