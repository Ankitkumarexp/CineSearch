
from flask import Blueprint, jsonify, request

from services.search_service import (
    search_movies,
    autocomplete_movies
)
from services.logging_service import add_search_log

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search", methods=["GET"])
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Please enter a movie name"
        }), 400

    results = search_movies(query)

    return jsonify({
        "query": query,
        "total_results": len(results),
        "results": results
    })


@search_bp.route("/api/autocomplete", methods=["GET"])
def autocomplete():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Please enter a search query"
        }), 400

    suggestions = autocomplete_movies(query)

    return jsonify({
        "query": query,
        "suggestions": suggestions,
        "total_suggestions": len(suggestions)
    })

@search_bp.route("/api/search-log", methods=["POST"])
def create_search_log():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    query = data.get("query", "").strip()

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        return jsonify({
            "error": "Valid user_id is required"
        }), 400

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    log = add_search_log(user_id, query)

    return jsonify({
        "message": "Search logged successfully",
        "log": log
    }), 201
