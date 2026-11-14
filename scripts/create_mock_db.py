# scripts/create_mock_db.py
import sqlite3
import os

def create_mock_db(db_path="cinesearch.db"):
    if os.path.exists(db_path):
        print(f"'{db_path}' already exists.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE movie (
            movie_id INTEGER PRIMARY KEY, 
            title TEXT NOT NULL
        );
        CREATE TABLE genre (
            genre_id INTEGER PRIMARY KEY, 
            genre_name TEXT NOT NULL
        );
        CREATE TABLE movie_genre (
            movie_id INTEGER, 
            genre_id INTEGER
        );

        INSERT INTO genre VALUES 
            (1, 'Animation'), 
            (2, 'Sci-Fi'), 
            (3, 'Adventure');
        
        INSERT INTO movie VALUES 
            (1, 'Toy Story (1995)'),
            (260, 'Star Wars: A New Hope (1977)'),
            (1196, 'Star Wars: The Empire Strikes Back (1980)'),
            (541, 'Blade Runner (1982)');

        INSERT INTO movie_genre VALUES 
            (1, 1), (1, 3), 
            (260, 2), (260, 3), 
            (1196, 2), (1196, 3), 
            (541, 2);
    """)
    conn.commit()
    conn.close()
    print("Mock 'cinesearch.db' created successfully!")

if __name__ == "__main__":
    create_mock_db()