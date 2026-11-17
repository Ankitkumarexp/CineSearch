
import sqlite3
import time
from pathlib import Path

from flask import Blueprint, jsonify, request

from services.search_service import (
    get_movie_by_id,
    get_movie_ratings
)

rating_bp = Blueprint("ratings", __name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "cinesearch.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Get all ratings for a movie
@rating_bp.route(
    "/api/movies/<int:movie_id>/ratings",
    methods=["GET"]
)
def movie_ratings(movie_id):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    ratings = get_movie_ratings(movie_id)

    movielens_ratings = [
        item for item in ratings
        if item["rating_source"] == "movielens"
    ]
    community_ratings = [
        item for item in ratings
        if item["rating_source"] == "community"
    ]
    

    movielens_average = (
        sum(item["rating"] for item in movielens_ratings)
        / len(movielens_ratings)
        if movielens_ratings else None
    )

    community_average = (
        sum(item["rating"] for item in community_ratings)
        / len(community_ratings)
        if community_ratings else None
    )

    user_id = request.args.get("user_id", type=int)

    your_rating = next(
        (
            item["rating"]
            for item in community_ratings
            if item["user_id"] == user_id
        ),
        None
    )

    return jsonify({
        "movie_id": movie_id,
        "movie_title": movie["title"],
        "average_rating": round(movielens_average, 2) if movielens_average is not None else None,
        "total_ratings": len(movielens_ratings),
        "movielens_average": round(movielens_average, 2) if movielens_average is not None else None,
        "movielens_total": len(movielens_ratings),
        "community_average": round(community_average, 2) if community_average is not None else None,
        "community_total": len(community_ratings),
        "your_rating": your_rating,
        "ratings": ratings
    }), 200



# Submit or update a movie rating
@rating_bp.route(
    "/api/movies/<int:movie_id>/ratings",
    methods=["POST"]
)
def submit_movie_rating(movie_id):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    rating = data.get("rating")

    if (
        not isinstance(user_id, int)
        or isinstance(user_id, bool)
        or user_id <= 0
    ):
        return jsonify({"error": "Valid user_id is required"}), 400

    if (
        isinstance(rating, bool)
        or not isinstance(rating, (int, float))
        or not 0.5 <= rating <= 5.0
    ):
        return jsonify({
            "error": "Rating must be between 0.5 and 5.0"
        }), 400

    connection = get_connection()

    try:
        connection.execute(
            "INSERT OR IGNORE INTO app_user (user_id) VALUES (?)",
            (user_id,)
        )

        connection.execute("""
            INSERT INTO rating (
                user_id, movie_id, rating, timestamp, rating_source
            )
            VALUES (?, ?, ?, ?, 'community')
            ON CONFLICT(user_id, movie_id)
            DO UPDATE SET
                rating_source = 'community',
                rating = excluded.rating,
                timestamp = excluded.timestamp
        """, (
            user_id,
            movie_id,
            float(rating),
            int(time.time())
        ))

        connection.commit()

        return jsonify({
            "message": "Movie rating saved successfully",
            "user_id": user_id,
            "movie_id": movie_id,
            "movie_title": movie["title"],
            "rating": float(rating)
        }), 201

    except sqlite3.Error:
        connection.rollback()
        return jsonify({
            "error": "Could not save movie rating"
        }), 500

    finally:
        connection.close()
