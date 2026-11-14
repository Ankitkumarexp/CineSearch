
# CineSearch – Database Design

## 1. Introduction

CineSearch is a movie search, ranking and recommendation project. This document explains the database design and database engineering work handled by Student 2.

The database stores movie information, genres, users, ratings and tags. It also supports efficient querying and movie statistics.

## 2. Technology Stack

- Python
- SQLite
- Pandas
- NumPy
- Matplotlib
- Google Colab

## 3. Dataset

The project uses the MovieLens 32M dataset provided by GroupLens Research.

Dataset link: https://grouplens.org/datasets/movielens/32m/

The dataset contains these main CSV files:

- movies.csv
- ratings.csv
- tags.csv
- links.csv

## 4. Database Tables

The relational database contains the following tables:

### 4.1 MOVIE

Stores basic information about movies.

- movie_id – Primary key
- title – Movie title
- release_year – Release year
- imdb_id – IMDb identifier
- tmdb_id – TMDB identifier

### 4.2 GENRE

Stores unique movie genres.

- genre_id – Primary key
- genre_name – Unique genre name

### 4.3 MOVIE_GENRE

Connects movies with their genres.

- movie_id – Foreign key referencing MOVIE
- genre_id – Foreign key referencing GENRE

The combination of movie_id and genre_id forms the composite primary key.

### 4.4 APP_USER

Stores user identifiers.

- user_id – Primary key

### 4.5 RATING

Stores ratings submitted by users.

- rating_id – Primary key
- user_id – Foreign key referencing APP_USER
- movie_id – Foreign key referencing MOVIE
- rating – Rating value
- timestamp – Rating timestamp

A user can submit only one rating for a particular movie.

### 4.6 TAG_EVENT

Stores tags submitted by users for movies.

- tag_id – Primary key
- user_id – Foreign key referencing APP_USER
- movie_id – Foreign key referencing MOVIE
- tag_text – Tag description
- timestamp – Tag timestamp

### 4.7 MOVIE_STATS

Stores precomputed movie statistics.

- movie_id – Primary key and foreign key
- rating_count – Total number of ratings
- average_rating – Average movie rating

## 5. Relationships

- One movie can have multiple genres.
- One genre can belong to multiple movies.
- One user can submit multiple ratings.
- One movie can receive ratings from multiple users.
- Users can submit multiple tags.
- Each movie can have one corresponding movie statistics record.

## 6. Database Normalization

The database uses separate tables for movies, genres, users, ratings and tags.

The MOVIE_GENRE table handles the many-to-many relationship between movies and genres.

This structure reduces unnecessary duplication and improves data consistency.

## 7. ETL Process

The ETL process consists of three main stages:

1. Extract data from MovieLens CSV files.
2. Transform the data into the required relational structure.
3. Load the processed records into SQLite tables.

The import process handles movies, genres, ratings and tags.

A reproducible ratings subset can be used to keep the workload manageable in Google Colab.

## 8. Indexing and Query Performance

Indexes are used to improve database query performance.

The project studies query execution before and after index creation.

SQLite's EXPLAIN QUERY PLAN is used to inspect how queries are executed.

Indexes can improve read performance, but they also require additional storage and can increase insertion and update costs.

## 9. Movie Statistics

The MOVIE_STATS table stores precomputed information such as rating count and average rating.

Precomputation can reduce repeated aggregate calculations when movie statistics are requested frequently.

## 10. Transactions and ACID Properties

Database transactions help maintain consistency during multi-step operations.

The project studies the ACID properties:

- Atomicity
- Consistency
- Isolation
- Durability

Invalid data operations are also used to examine database constraints.

## 11. Scalability and Storage

The project examines how database size and query performance change as the amount of data increases.

It also considers the storage overhead introduced by indexes and precomputed statistics.

## 12. Scope of Student 2

Student 2 is responsible for:

- Database schema design
- Data import and ETL
- SQL queries
- Database indexing
- Query performance analysis
- Precomputed movie statistics
- Transactions and ACID properties
- Database validation
- Scalability and storage analysis

Search algorithms, ranking, recommendation logic, API and frontend are handled by separate project workstreams.
