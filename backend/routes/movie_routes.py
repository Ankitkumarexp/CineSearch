
from flask import Blueprint, jsonify, redirect

from services.search_service import get_movie_by_id
from services.poster_service import get_movie_poster

movie_bp = Blueprint("movies", __name__)


@movie_bp.route("/api/movies/<int:movie_id>", methods=["GET"])
def movie_details(movie_id):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        return jsonify({
            "error": "Movie not found"
        }), 404

    return jsonify({
        "movie": movie
    }), 200


@movie_bp.route("/api/movies/<int:movie_id>/poster", methods=["GET"])
def movie_poster(movie_id):

    poster_url = get_movie_poster(movie_id)

    if not poster_url:
        return "", 404

    return redirect(poster_url, code=302)
