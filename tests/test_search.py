from search.preprocessing import tokenize
from search.inverted_index import InvertedIndex
from search.trie import PrefixTrie
from search.topk import get_top_k

def test_tokenizer_and_stopwords():
    text = "Toy Story (1995)! An animated adventure film."
    tokens = tokenize(text)
    assert "toy" in tokens and "animated" in tokens
    assert "an" not in tokens  # Stopword drop hona chahiye

def test_inverted_index_and_boolean_search():
    idx = InvertedIndex()
    idx.add_document(1, "toy story animation adventure comedy pixar toys")
    idx.add_document(2, "jumanji adventure fantasy magic board game")
    idx.add_document(3, "space jam animation adventure comedy space alien")

    res_and = idx.boolean_and(["animation", "adventure"])
    assert res_and == {1, 3}

    res_or = idx.boolean_or(["magic", "pixar"])
    assert res_or == {1, 2}

def test_prefix_trie_autocomplete():
    trie = PrefixTrie()
    trie.insert("Toy Story (1995)")
    trie.insert("Toy Story 2 (1999)")
    trie.insert("Space Jam (1996)")
    trie.insert("Spider-Man (2002)")

    prefix_res = trie.search_prefix("toy")
    assert len(prefix_res) == 2
    assert "Toy Story (1995)" in prefix_res

def test_top_k_min_heap_selector():
    dummy_scores = {101: 0.45, 102: 0.89, 103: 0.12, 104: 0.95, 105: 0.77}
    top_2 = get_top_k(dummy_scores, k=2)
    assert top_2 == [(104, 0.95), (102, 0.89)]