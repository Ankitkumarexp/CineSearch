# CineSearch frontend

## Included
- `index.html`: movie search page
- `style.css`: responsive styling
- `script.js`: backend search, autocomplete suggestions, genre/rating filters, and result cards

## Run locally
1. Start the Flask backend.
2. Open this folder in VS Code.
3. Open `index.html` with the Live Server extension.
4. The frontend expects Flask at `http://127.0.0.1:5000`.

## API contract
Uses `GET /api/health` and `GET /api/search?q=<keyword>`.
Search response should include `results`, with movie objects containing `title`, `year`,
`genre` (list or comma-separated string), and optionally `rating` or `vote_average`.

## Important compatibility notes
- Your current Search API returns `title`, `year`, and `genre`; it may not return a rating.
  The page displays “Rating not available” until the backend/database supplies a numeric rating.
- Genre and rating filters work on the movies currently returned by the search endpoint.
- Autocomplete calls the existing search endpoint after a 250 ms pause and uses returned titles as suggestions.
- If the browser reports a CORS error, configure Flask-CORS for local development:
  `pip install flask-cors`; then add `from flask_cors import CORS` and `CORS(app)` after creating `app`.
