
# Temporary movie data for API testing

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


# Search movies by title
def search_movies(query):

    query = query.strip().lower()

    if not query:
        return []

    results = [
        movie for movie in movies
        if query in movie["title"].lower()
    ]

    return results


# Generate autocomplete suggestions
def autocomplete_movies(query, limit=5):

    query = query.strip().lower()

    if not query:
        return []

    results = [
        movie["title"]
        for movie in movies
        if movie["title"].lower().startswith(query)
    ]

    return results[:limit]

# Get movie details using movie ID
def get_movie_by_id(movie_id):

    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    return None

# Temporary ratings for API integration testing
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
