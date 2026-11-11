# CineSearch — Software Testing Report

## 1. Introduction

This document describes the automated testing performed on the CineSearch application.

The purpose of testing is to verify the functionality of the Flask backend, validate API responses, test frontend interactions, identify errors and ensure that the application behaves as expected.

Both backend API testing and frontend browser testing have been performed.

## 2. Testing Environment

| Component | Technology |
|---|---|
| Programming Language | Python 3.14.10 |
| Backend Framework | Flask |
| Backend Testing Framework | Pytest 9.2.0 |
| Frontend Testing Framework | Playwright |
| Coverage Tool | pytest-cov 7.1.0 |
| Frontend | HTML, CSS, JavaScript |
| Operating System | Windows |
| API Format | JSON |
| Browser Testing | Chromium (Headless) |

## 3. Testing Approach

Two types of automated testing were performed.

### 3.1 Backend API Testing

Backend testing was performed using Pytest and Flask's built-in test client.

The test client sends HTTP requests directly to the Flask application without requiring the development server to run separately.

Testing includes:
- Functional testing
- API response validation
- Input validation
- Error handling
- Search functionality testing
- Search history testing
- Movie ratings testing

### 3.2 Frontend Browser Testing

Frontend testing was performed using Playwright with Chromium.

These tests simulate user interactions with the CineSearch website and verify that the frontend works correctly with the backend API.

Testing includes:
- Frontend page loading
- Search input and button
- Search functionality
- Autocomplete suggestions
- Movie details popup
- Popup closing functionality
- Search history section
- Filter controls

## 4. Backend Test Cases

A total of 22 automated backend test cases were executed.

| No. | Test Case | Expected Result |
|---|---|---|
| 1 | Homepage | HTTP 200 |
| 2 | Backend health check | Healthy status |
| 3 | Movie search | Matching results |
| 4 | Search without query | HTTP 400 |
| 5 | Movie autocomplete | Suggestions returned |
| 6 | Movie details | Movie information returned |
| 7 | Invalid movie ID | HTTP 404 |
| 8 | Movie ratings | Rating information returned |
| 9 | Search history workflow | Save, retrieve and delete successfully |
| 10 | Autocomplete without query | HTTP 400 |
| 11 | Search log without JSON | HTTP 400 |
| 12 | Search log without user ID | HTTP 400 |
| 13 | Search log with zero user ID | HTTP 400 |
| 14 | Search log with negative user ID | HTTP 400 |
| 15 | Search log with Boolean user ID | HTTP 400 |
| 16 | Search log with string user ID | HTTP 400 |
| 17 | Search log with empty query | HTTP 400 |
| 18 | Empty search service query | Empty result |
| 19 | Empty autocomplete query | Empty result |
| 20 | Autocomplete result limit | Limited suggestions |
| 21 | Movie without ratings | Zero average rating |
| 22 | Ratings for missing movie | HTTP 404 |

## 5. Frontend Test Cases

A total of 11 automated frontend test cases were executed using Playwright.

| No. | Test Case | Expected Result |
|---|---|---|
| 1 | Frontend page loading | Page loads successfully |
| 2 | Search input | Search field is available |
| 3 | Search button | Button is available |
| 4 | Filter controls | Filters are visible |
| 5 | Search history section | History section is available |
| 6 | Movie details modal | Modal element exists |
| 7 | Search for Interstellar | Matching movie displayed |
| 8 | Search for Inception | Matching movie displayed |
| 9 | Autocomplete functionality | Suggestions displayed |
| 10 | Movie details popup | Popup opens successfully |
| 11 | Close movie popup | Popup closes successfully |

## 6. Test Execution

### 6.1 Backend Test Execution

Command:

```powershell
python -m pytest tests/test_api.py -v
```

Result:

- Total tests: 22
- Passed: 22
- Failed: 0

**Overall result: All 22 backend tests passed.**

### 6.2 Frontend Test Execution

The Flask backend must be running before executing the frontend tests. The Playwright test fixture starts its own frontend server.

Command:

```powershell
python -m pytest tests/test_frontend.py -v
```

Result:

- Total tests: 11
- Passed: 11
- Failed: 0
- Execution time: 23.51 seconds

**Overall result: All 11 frontend tests passed.**

### 6.3 Combined Testing Summary

| Testing Category | Total Tests | Passed | Failed |
|---|---:|---:|---:|
| Backend API Testing | 22 | 22 | 0 |
| Frontend Browser Testing | 11 | 11 | 0 |
| **Total** | **33** | **33** | **0** |

**Overall result: All 33 automated tests passed.**

## 7. Code Coverage Analysis

Backend code coverage was generated using:

```powershell
python -m pytest --cov=app --cov=routes --cov=services --cov-report=term-missing tests/test_api.py
```

### Module-wise Coverage

| Module | Coverage |
|---|---:|
| app.py | 95% |
| routes/__init__.py | 100% |
| movie_routes.py | 100% |
| rating_routes.py | 100% |
| search_routes.py | 100% |
| user_routes.py | 100% |
| services/__init__.py | 100% |
| logging_service.py | 100% |
| search_service.py | 100% |
| **Overall Backend** | **99%** |

## 8. Coverage Summary

The backend contains 113 executable statements.

- Executed statements: 112
- Missed statements: 1
- Overall backend coverage: 99%

The only uncovered statement is the Flask development-server startup instruction:

```python
app.run(debug=True)
```

This statement is normally not executed during API tests because the Flask test client is used instead.

Note: The 99% coverage figure represents backend code coverage only. Frontend browser tests are not included in this calculation.

## 9. Testing Results

The automated tests confirm that:

1. The Flask backend responds successfully.
2. Movie search and autocomplete work correctly.
3. Movie details can be retrieved.
4. Movie ratings are calculated and returned.
5. Invalid movie IDs are handled correctly.
6. Search history can be saved and retrieved.
7. Search history can be cleared.
8. Invalid search-log requests are rejected.
9. Empty queries are handled safely.
10. The frontend loads successfully.
11. Users can search for movies through the interface.
12. Autocomplete suggestions work.
13. Movie details can be viewed in a popup.
14. The movie popup can be closed.

## 10. Current Limitations

The current testing results apply to the existing implementation and temporary test data.

The following areas still require testing during final integration:

- Persistent database operations
- Full MovieLens dataset integration
- Student 1's search algorithm
- Student 3's ranking and recommendation algorithms
- End-to-end integration with final production data
- Performance under multiple simultaneous users

Search history currently uses in-memory storage and resets when the Flask server restarts.

## 11. Conclusion

The CineSearch application has successfully passed 33 automated test cases, including 22 backend API tests and 11 frontend browser tests.

The backend achieved an overall code coverage of 99%.

These results provide a reliable foundation for identifying errors, validating application functionality and supporting future development.

Further testing will be performed after integration of the database, search algorithms and recommendation modules.

**Testing status: Initial backend and frontend automated testing completed successfully.**