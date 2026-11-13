
# CineSearch
### A Database-Driven Search, Ranking and Recommendation Engine

CineSearch is a movie search, ranking and recommendation project built using the MovieLens dataset. It focuses on organizing movie data, efficient database operations, search performance and recommendation-related functionality.

## Project Overview

The project is divided into multiple workstreams:

- Database Management and Data Engineering
- Search and Retrieval
- Ranking and Recommendation
- Backend Development
- Frontend Development

## Technology Stack

- Python
- SQLite
- Pandas
- NumPy
- Matplotlib
- SQL

## Dataset

The project uses the MovieLens 32M dataset provided by GroupLens Research.

Official dataset:
https://grouplens.org/datasets/movielens/32m/

Main dataset files:

- movies.csv
- ratings.csv
- tags.csv
- links.csv

See [data/README.md](data/README.md) for download instructions.

## Repository Structure

```text
CineSearch/
│
├── backend/
├── data/
│   └── README.md
│
├── database/
│   ├── schema.sql
│   ├── indexes.sql
│   ├── import_data.py
│   ├── queries.py
│   ├── performance.py
│   ├── movie_stats.py
│   ├── transactions.py
│   ├── scalability.py
│   └── validation.py
│
├── docs/
│   ├── database_design.md
│   └── er_diagram.md
│
├── experiments/
│   ├── database_performance.ipynb
│   └── search_performance.py
│
├── frontend/
├── scripts/
├── search/
│
├── tests/
│   ├── test_database.py
│   └── test_search.py
│
├── requirements.txt
└── README.md
```

## Student 2 – Database Engineering

Student 2 is responsible for database management, data engineering and performance analysis.

Main contributions:

1. Relational database schema design.
2. Primary key and foreign key constraints.
3. MovieLens dataset ETL and data import.
4. SQL queries and data retrieval.
5. Database indexing and query optimization.
6. Query execution plan analysis.
7. Precomputed movie statistics.
8. Database transactions and ACID properties.
9. Database validation.
10. Scalability and storage analysis.

## Database Documentation

- [Database Design](docs/database_design.md)
- [Entity Relationship Diagram](docs/er_diagram.md)

## Installation

Install the required Python dependencies:

```bash
py -m pip install -r requirements.txt
```

## Dataset Setup

1. Download the MovieLens 32M dataset.
2. Extract the downloaded ZIP file.
3. Place the required CSV files in the data directory.
4. Run the database import scripts after configuring the dataset paths.

The original dataset is large and is not stored directly in this repository.

## Running Tests

Run the Python test suite from the project root:

```bash
py -m unittest discover -s tests -p "test_*.py" -v
```

## Database Experiment Notebook

The complete Student 2 database engineering notebook is available at:

`experiments/database_performance.ipynb`

It contains database design, ETL, SQL queries, indexing, performance experiments, transactions and scalability analysis.

## Project Scope

CineSearch combines database engineering with search and recommendation-related components.

Database management, search algorithms, ranking, recommendation logic, backend and frontend are maintained as separate project workstreams.

## Contributors

CineSearch is developed as a collaborative student project.

## Team Contributions

The CineSearch project is developed collaboratively, with each student responsible for a specific workstream.

### Student 1 – Search and Retrieval
- Data preprocessing
- Inverted Index implementation
- Trie implementation
- Search ranking
- Top-K retrieval

### Student 2 – Database and Data Engineering
- MovieLens dataset handling
- Relational database schema design
- ETL and data import
- SQL queries and indexing
- Query performance analysis
- Transactions and ACID properties
- Database scalability and validation

### Student 3 – Recommendation System
- Popularity-based recommendations
- Genre affinity
- Co-occurrence-based recommendations

### Student 4 – Backend and Frontend
- Backend development
- Frontend development
- Application integration

### Shared Responsibilities
- Project integration
- Documentation
- Experiments and performance evaluation
- Testing and validation

