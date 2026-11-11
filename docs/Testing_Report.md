
# CineSearch — Software Testing Report

## 1. Introduction

This document describes the automated testing performed on the CineSearch application.

The purpose of testing is to verify the functionality of the Flask backend, validate API responses, identify errors and ensure that the application behaves as expected.

## 2. Testing Environment

| Component | Technology |
|---|---|
| Programming Language | Python 3.14.10 |
| Backend Framework | Flask |
| Testing Framework | Pytest 9.2.0 |
| Coverage Tool | pytest-cov 7.1.0 |
| Frontend | HTML, CSS, JavaScript |
| Operating System | Windows |
| API Format | JSON |

## 3. Testing Approach

Automated API testing was performed using Pytest and Flask's built-in test client.

The test client sends HTTP requests directly to the Flask application without requiring the development server to run separately.

The testing process includes:

- Functional testing
- API response validation
- Input validation
- Error handling
- Search functionality testing
- Search history testing
- Movie ratings testing

## 4. Test Cases

A total of 22 automated test cases were executed.

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

## 5. Test Execution

The following command was used to execute the automated test suite:

```powershell
python -m pytest tests/test_api.py -v
```

Result:

- Total tests: 22
- Passed: 22
- Failed: 0
- Execution time: 0.19 seconds

**Overall result: All 22 tests passed.**

## 6. Code Coverage Analysis

The coverage report was generated using:

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

## 7. Coverage Summary

The backend contains 113 executable statements.

- Executed statements: 112
- Missed statements: 1
- Overall coverage: 99%

The only uncovered statement is the Flask development-server startup instruction:

```python
app.run(debug=True)
```

This statement is normally not executed during API tests because the Flask test client is used instead.

## 8. Testing Results

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

## 9. Current Limitations

The current testing results apply to the existing backend implementation and temporary test data.

The following areas still require testing during final integration:

- Persistent database operations
- Full MovieLens dataset integration
- Student 1's search algorithm
- Student 3's ranking and recommendation algorithms
- End-to-end integration with final production data
- Performance under multiple simultaneous users

Search history currently uses in-memory storage and resets when the Flask server restarts.

## 10. Conclusion

The CineSearch backend has successfully passed 22 automated test cases with an overall code coverage of 99%.

The testing framework provides a reliable foundation for identifying errors and validating future changes.

Further testing will be performed after the integration of the database, search algorithms and recommendation modules.

**Testing status: Initial backend testing completed successfully.**
