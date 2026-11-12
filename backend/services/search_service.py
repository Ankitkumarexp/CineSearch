
from search.preprocessing import tokenize
from search.inverted_index import InvertedIndex
from search.trie import PrefixTrie

# Temporary movie data for API testing.
# Student 2's SQLite database will replace this later.

movies = [
    {
        "id": 1,
        "title": "Toy Story",
        "year": 1995,
        "genre": "Animation, Comedy"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "year": 2014,
        "genre": "Adventure, Sci-Fi"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action, Drama"
    },
    {
        "id": 4,
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Sci-Fi"
    }
]

# Build Student 1's search structures.
movie_index = InvertedIndex()
movie_trie = PrefixTrie()

movie_lookup = {
    movie["id"]: movie
    for movie in movies
}

for movie in movies:
    movie_index.add_document(
        movie["id"],
        movie["title"]
    )

    movie_trie.insert(movie["title"])


# Search movies using Boolean AND or OR.
def search_movies(query, mode="and"):

    if not query or not query.strip():
        return []

    query = query.strip()
    tokens = tokenize(query)

    # Preserve substring matching for stop-word-only queries.
    if not tokens:
        return [
            movie for movie in movies
            if query.lower() in movie["title"].lower()
        ]

    if mode == "or":
        matched_ids = movie_index.boolean_or(tokens)
    else:
        matched_ids = movie_index.boolean_and(tokens)

    return [
        movie_lookup[movie_id]
        for movie_id in movie_lookup
        if movie_id in matched_ids
    ]


# Generate autocomplete using Student 1's Trie.
def autocomplete_movies(query, limit=5):

    if not query or not query.strip():
        return []

    if limit <= 0:
        return []

    return movie_trie.search_prefix(query, limit)


# Get movie details using movie ID.
def get_movie_by_id(movie_id):

    return movie_lookup.get(movie_id)


# Temporary ratings for API testing.
ratings_data = {
    1: [
        {"user_id": 101, "rating": 4.5},
        {"user_id": 102, "rating": 4.0},
        {"user_id": 103, "rating": 5.0}
    ],
    2: [
        {"user_id": 101, "rating": 5.0},
        {"user_id": 104, "rating": 4.5}
    ]
}


def get_movie_ratings(movie_id):

    return ratings_data.get(movie_id, [])
