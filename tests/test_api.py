
import sys
from pathlib import Path

import pytest

# Add the backend directory to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_movie_search(client):
    response = client.get("/api/search?q=Interstellar")

    assert response.status_code == 200
    assert response.json["total_results"] >= 1
    assert isinstance(response.json["results"], list)


def test_search_without_query(client):
    response = client.get("/api/search")

    assert response.status_code == 400


def test_autocomplete(client):
    response = client.get("/api/autocomplete?q=In")

    assert response.status_code == 200
    assert isinstance(response.json["suggestions"], list)


def test_movie_details(client):
    response = client.get("/api/movies/1")

    assert response.status_code == 200
    assert response.json is not None


def test_movie_not_found(client):
    response = client.get("/api/movies/999999")

    assert response.status_code == 404


def test_movie_ratings(client):
    response = client.get("/api/movies/1/ratings")

    assert response.status_code == 200
    assert response.json is not None


def test_search_history_workflow(client):
    user_id = 987654321

    # Remove any previous test history.
    client.delete(f"/api/users/{user_id}/history")

    # Save a search.
    save_response = client.post(
        "/api/search-log",
        json={
            "user_id": user_id,
            "query": "Interstellar"
        }
    )

    assert save_response.status_code == 201

    # Retrieve search history.
    history_response = client.get(
        f"/api/users/{user_id}/history"
    )

    assert history_response.status_code == 200
    assert history_response.json["total_searches"] == 1
    assert history_response.json["history"][0]["query"] == "Interstellar"

    # Clear search history.
    delete_response = client.delete(
        f"/api/users/{user_id}/history"
    )

    assert delete_response.status_code == 200
    assert delete_response.json["deleted_count"] == 1

    # Verify history is empty.
    final_response = client.get(
        f"/api/users/{user_id}/history"
    )

    assert final_response.status_code == 200
    assert final_response.json["total_searches"] == 0
