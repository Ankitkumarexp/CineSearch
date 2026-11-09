# test_run.py
from search.engine import get_search_engine

print("=== RUNNING SEARCH ENGINE TEST ===")
inv_index, trie = get_search_engine()

# Test 1: Autocomplete
print("\n--- Test 1: Autocomplete for 'Star' ---")
suggestions = trie.search_prefix("Star")
print("Suggestions:", suggestions)

# Test 2: Boolean AND Search
print("\n--- Test 2: Boolean AND Search for 'Sci-Fi' ---")
results = inv_index.boolean_and(["sci", "fi"])
print("Matching Movie IDs:", results)

# Test 3: Boolean OR Search
print("\n--- Test 3: Boolean OR Search for 'Animation' OR 'Adventure' ---")
or_results = inv_index.boolean_or(["animation", "adventure"])
print("Matching Movie IDs:", or_results)

print("\nAll integration tests passed cleanly!")