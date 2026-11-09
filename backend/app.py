
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)

# Enable communication with frontend
CORS(app)


# 1. HOME API
@app.route("/")
def home():
    return jsonify({
        "project": "CineSearch",
        "message": "Backend is running successfully!"
    })


# 2. HEALTH CHECK API
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "CineSearch API"
    })


# 3. TEMPORARY MOVIE DATA
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


# 4. MOVIE SEARCH API
@app.route("/api/search", methods=["GET"])
def search_movies():

    # Get search query
    query = request.args.get("q", "").strip().lower()

    # Validate search query
    if not query:
        return jsonify({
            "error": "Please enter a movie name"
        }), 400

    # Search matching movies
    results = [
        movie for movie in movies
        if query in movie["title"].lower()
    ]

    # Return search results
    return jsonify({
        "query": query,
        "total_results": len(results),
        "results": results
    })


# 5. START FLASK SERVER
if __name__ == "__main__":
    app.run(debug=True)