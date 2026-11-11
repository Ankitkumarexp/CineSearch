
# CineSearch — Team Integration Guide

## 1. Purpose

This document explains how the four team members will integrate their modules into the CineSearch application.

The goal is to connect the search algorithms, database, ranking system, Flask backend and frontend without breaking existing functionality.

## 2. Current Architecture

Frontend (HTML, CSS, JavaScript)
        |
        | HTTP requests / JSON
        v
Flask Backend (Student 4)
        |
        +-- Search Service (Student 1)
        |
        +-- Database Layer (Student 2)
        |
        +-- Ranking & Recommendation (Student 3)
        |
        +-- API Integration & Testing (Student 4)

The backend currently uses temporary movie and rating data. These will be replaced when the relevant modules are ready.

## 3. Student 1 — Search Algorithm Integration

### Responsibility

Student 1 develops the movie search algorithms, including the inverted index and other search-related data structures.

### Expected Python Interface

```python
def search_movies(query):
    """
    Accepts a movie title or keyword.
    Returns a list of matching movie dictionaries.
    """
    pass

def autocomplete_movies(query, limit=5):
    """
    Returns up to 'limit' movie suggestions.
    """
    pass
```

### Expected Movie Format

```json
{
  "id": 2,
  "title": "Interstellar",
  "year": 2014,
  "genre": "Adventure, Sci-Fi"
}
```

### Integration Point

`backend/services/search_service.py`

Student 4 will connect Student 1's algorithm through the existing search service interface.

The following APIs should continue working:

- `GET /api/search?q=Interstellar`
- `GET /api/autocomplete?q=In`

## 4. Student 2 — Database Integration

### Responsibility

Student 2 handles:

- SQLite database setup
- Movie and rating data storage
- Dataset import
- Database queries
- Persistent search history, if included in the agreed database design

### Expected Database Functions

```python
def get_movie_by_id(movie_id):
    """Returns a movie dictionary or None."""
    pass

def get_movie_ratings(movie_id):
    """Returns rating records for the movie."""
    pass

def get_all_movies():
    """Returns movie records for indexing/search."""
    pass
```

### Expected Rating Format

```json
{
  "user_id": 101,
  "rating": 4.5
}
```

### Integration Point

A database access module, with its final location agreed upon by the team.

The following APIs must remain compatible:

- `GET /api/movies/<movie_id>`
- `GET /api/movies/<movie_id>/ratings`
- `GET /api/users/<user_id>/history`
- `DELETE /api/users/<user_id>/history`

The database module should not directly modify frontend files or Flask route definitions.

## 5. Student 3 — Ranking and Recommendation Integration

### Responsibility

Student 3 develops movie ranking and recommendation algorithms.

### Proposed Python Interface

```python
def rank_movies(query, movies):
    """
    Accepts a search query and matching movies.
    Returns movies ordered by relevance.
    """
    pass

def recommend_movies(movie_id, limit=5):
    """
    Accepts a movie ID.
    Returns up to 'limit' recommended movies.
    """
    pass
```

### Expected Output

Ranking should return movie dictionaries in the same format used by the search API.

Recommendations should also return movie dictionaries with valid movie IDs.

### Integration Point

A dedicated ranking or recommendation service.

Student 4 will connect ranking to the existing search API once the algorithm is available.

A recommendation API may be added later after agreeing on the request and response format.

## 6. Student 4 — Backend and Frontend Integration

### Responsibilities

- Maintain Flask application structure
- Connect team modules to backend services
- Maintain REST API endpoints
- Integrate backend responses with frontend
- Handle errors and invalid requests
- Perform API and frontend testing
- Coordinate final integration

### Existing Backend Structure

```text
backend/
    app.py
    routes/
        __init__.py
        search_routes.py
        movie_routes.py
        rating_routes.py
        user_routes.py
    services/
        __init__.py
        search_service.py
        logging_service.py
```

### Existing Frontend Structure

```text
frontend/
    index.html
    style.css
    script.js
```

## 7. Shared Data Contract

All integrated modules should use consistent field names.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique movie ID |
| title | String | Movie title |
| year | Integer | Release year |
| genre | String | Comma-separated genres |
| user_id | Integer | User identifier |
| rating | Number | Movie rating |

The final dataset may contain additional fields. Required API fields should remain consistent.

## 8. Integration Sequence

### Phase 1 — Search

1. Receive Student 1's search module.
2. Confirm its input and output formats.
3. Connect it to the Flask search service.
4. Test search and autocomplete.

### Phase 2 — Database

1. Receive Student 2's database module.
2. Verify database file paths and schema.
3. Replace temporary movie and rating data.
4. Test movie details and ratings.
5. Test persistence where implemented.

### Phase 3 — Ranking

1. Receive Student 3's ranking module.
2. Connect ranking to search results.
3. Test result ordering.
4. Add recommendation integration if required.

### Phase 4 — Final Testing

1. Test all existing APIs.
2. Test invalid inputs and missing movies.
3. Test frontend search and autocomplete.
4. Test movie details and ratings.
5. Test search history.
6. Check that integrated modules work together.

## 9. Git Collaboration Rules

- Each student should work on their own feature branch.
- Avoid directly editing another student's module without coordination.
- Commit completed and tested changes.
- Review changes before merging into the shared branch.
- Resolve merge conflicts carefully.
- Do not commit large datasets, temporary files or local environment folders.

## 10. Current Project Status

Completed by Student 4:

- Flask backend setup
- Modular route structure
- Search and autocomplete APIs
- Movie details and ratings APIs
- Search history APIs
- Frontend integration
- API documentation
- Git commits

Pending:

- Student 1 search algorithm integration
- Student 2 persistent database integration
- Student 3 ranking and recommendation integration
- Full dataset testing
- Final end-to-end integration

## 11. Important Notes

The interfaces in this document are proposed integration contracts, not proof that teammate modules have already implemented them.

Before integration, each student should confirm their actual function names, parameters, return values and file locations.

Student 4 should adapt the integration layer rather than unnecessarily rewriting teammates' algorithms.

The existing working application should be preserved until replacement modules have passed testing.
