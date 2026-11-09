# search/engine.py
import sqlite3
import pickle
import os
import time
from search.preprocessing import clean_text
from search.inverted_index import InvertedIndex
from search.trie import PrefixTrie

CACHE_DIR = "data"
CACHE_FILE = os.path.join(CACHE_DIR, "search_cache.pkl")

def build_from_db(db_path="cinesearch.db"):
    """Database se movies padhkar InvertedIndex aur Trie populate karta hai"""
    print(f"Reading from database '{db_path}'...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """
        SELECT m.movie_id, m.title, IFNULL(GROUP_CONCAT(g.genre_name, ' '), '')
        FROM movie m
        LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
        LEFT JOIN genre g ON mg.genre_id = g.genre_id
        GROUP BY m.movie_id;
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    inv_index = InvertedIndex()
    trie = PrefixTrie()

    for movie_id, title, genres in rows:
        # Trie me sirf title pass karo (sirf 1 argument)
        trie.insert(title)

        # Inverted index me movie_id aur clean tokens pass karo
        doc_text = f"{title} {genres}"
        tokens = clean_text(doc_text)
        inv_index.add_document(movie_id, tokens)

    print(f"Successfully indexed {len(rows)} movies.")
    return inv_index, trie

def get_search_engine(db_path="cinesearch.db", force_rebuild=False):
    """Disk cache se turant load karega; cache na ho toh DB se banakar save karega"""
    os.makedirs(CACHE_DIR, exist_ok=True)

    if not force_rebuild and os.path.exists(CACHE_FILE):
        print("Loading search engine from disk cache...")
        t0 = time.time()
        with open(CACHE_FILE, "rb") as f:
            inv_index, trie = pickle.load(f)
        print(f"Loaded from cache in {time.time() - t0:.4f}s.")
        return inv_index, trie

    print("Building new search structures...")
    inv_index, trie = build_from_db(db_path)
    with open(CACHE_FILE, "wb") as f:
        pickle.dump((inv_index, trie), f)
    print("Saved search engine to disk cache.")

    return inv_index, trie