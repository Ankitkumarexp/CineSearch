
# CineSearch API Documentation

## 1. Project Overview

CineSearch is a movie search and recommendation system.

The backend is developed using Python Flask. The frontend communicates with the backend through REST APIs.

**Base URL:** `http://127.0.0.1:5000`

## 2. Technology Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- API communication: REST API, JSON
- Database: SQLite (planned integration)
- Search and recommendation algorithms: Developed by team members

## 3. API Endpoints

### 3.1 Health Check

**Endpoint:** `GET /api/health`

**Purpose:** Checks whether the backend server is running.

Example response:

```json
{
  "status": "healthy",
  "service": "CineSearch API"
}
```

### 3.2 Search Movies

**Endpoint:** `GET /api/search?q=movie_name`

**Purpose:** Searches movies using a search query.

Example:

`GET /api/search?q=Interstellar`

Example response:

```json
{
  "query": "Interstellar",
  "total_results": 1,
  "results": [
    {
      "id": 2,
      "title": "Interstellar",
      "year": 2014,
      "genre": "Adventure, Sci-Fi"
    }
  ]
}
```

### 3.3 Movie Autocomplete

**Endpoint:** `GET /api/autocomplete?q=movie_name`

**Purpose:** Returns movie suggestions while the user types.

Example:

`GET /api/autocomplete?q=In`

Example response:

```json
{
  "query": "In",
  "suggestions": [
    {
      "id": 2,
      "title": "Interstellar",
      "year": 2014,
      "genre": "Adventure, Sci-Fi"
    },
    {
      "id": 4,
      "title": "Inception",
      "year": 2010,
      "genre": "Action, Sci-Fi"
    }
  ],
  "total_suggestions": 2
}
```

### 3.4 Get Movie Details

**Endpoint:** `GET /api/movies/<movie_id>`

**Purpose:** Retrieves details of a movie using its ID.

Example:

`GET /api/movies/1`

### 3.5 Get Movie Ratings

**Endpoint:** `GET /api/movies/<movie_id>/ratings`

**Purpose:** Retrieves rating information for a movie.

Example:

`GET /api/movies/1/ratings`

### 3.6 Save Search History

**Endpoint:** `POST /api/search-log`

**Purpose:** Saves a user's search query.

Request body:

```json
{
  "user_id": 101,
  "query": "Interstellar"
}
```

### 3.7 Get User Search History

**Endpoint:** `GET /api/users/<user_id>/history`

**Purpose:** Retrieves previous searches of a particular user.

Example:

`GET /api/users/101/history`

### 3.8 Clear User Search History

**Endpoint:** `DELETE /api/users/<user_id>/history`

**Purpose:** Deletes the search history of a particular user.

Example:

`DELETE /api/users/101/history`

## 4. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Invalid request |
| 404 | Resource not found |
| 500 | Internal server error |

## 5. Team Integration Responsibilities

| Team Member | Responsibility | Integration Point |
|---|---|---|
| Student 1 | Search algorithms | Search service |
| Student 2 | Database management | Data access layer |
| Student 3 | Ranking and recommendations | Ranking service |
| Student 4 | Backend APIs, frontend and integration | Flask routes and frontend |

## 6. Integration Guidelines

- All API responses should use JSON.
- Search algorithms should return structured movie results.
- Database operations should be handled through the database layer.
- Ranking algorithms should accept movie search results and return ranked results.
- The frontend should communicate with the backend using API requests.
- Existing API response formats should be preserved where possible.
- Any changes to API contracts should be discussed with the team.

## 7. Current Development Status

The following features have been implemented and tested with temporary data:

- Flask backend setup
- Movie search API
- Autocomplete API
- Movie details API
- Movie ratings API
- Search history API
- Clear search history API
- Frontend and backend integration
- Movie details popup
- Search history interface

**Important:** Current movie and rating data are temporary mock data. Search history is stored in memory and resets when the backend restarts. Persistent database integration and teammate module integration are pending.

## 8. Running the Project

Open a terminal in the project root.

Start the backend:

```powershell
python backend/app.py
```

Start the frontend in another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Open the frontend:

`http://127.0.0.1:5500`

Backend API:

`http://127.0.0.1:5000`
