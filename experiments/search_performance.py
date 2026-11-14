# experiments/search_performance.py
import sqlite3
import time
from search.engine import get_search_engine
from search.preprocessing import clean_text

def benchmark_sql_like(db_path: str, term: str) -> float:
    """Measures latency of SQL LIKE '%term%' full table scan in milliseconds."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    t0 = time.perf_counter()
    
    cur.execute("SELECT movie_id, title FROM movie WHERE LOWER(title) LIKE ?;", (f"%{term.lower()}%",))
    _ = cur.fetchall()
    
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    conn.close()
    return elapsed_ms

def benchmark_inverted_index(inv_index, term: str) -> float:
    """Measures latency of Inverted Index dictionary lookup in milliseconds."""
    tokens = clean_text(term)
    t0 = time.perf_counter()
    
    # InvertedIndex boolean_and lookup
    _ = inv_index.boolean_and(tokens)
    
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms

def run_performance_experiments(db_path="cinesearch.db"):
    print("=" * 70)
    print(" CINESEARCH EXPERIMENT 5 & 6: SQL LIKE VS INVERTED INDEX LATENCY")
    print("=" * 70)
    
    # Search engine load karo (disk cache se instant aayega)
    inv_index, _ = get_search_engine(db_path)

    test_queries = ["Star", "Sci-Fi", "Adventure", "Animation"]

    print(f"{'Query Term':<15} | {'SQL LIKE (ms)':<16} | {'Inverted Index (ms)':<20} | {'Speedup':<10}")
    print("-" * 70)

    for q in test_queries:
        # SQL measure karo
        sql_ms = benchmark_sql_like(db_path, q)
        # Inverted Index measure karo
        idx_ms = benchmark_inverted_index(inv_index, q)
        
        speedup = (sql_ms / idx_ms) if idx_ms > 0 else 1.0
        print(f"{q:<15} | {sql_ms:<16.4f} | {idx_ms:<20.4f} | {speedup:<10.1f}x")

    print("=" * 70)
    print("Empirical benchmarking completed successfully.")

if __name__ == "__main__":
    run_performance_experiments()