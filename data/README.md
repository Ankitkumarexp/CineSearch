
# CineSearch Dataset

## Dataset Source

CineSearch uses the MovieLens 32M dataset provided by GroupLens Research.

Official dataset page:
https://grouplens.org/datasets/movielens/32m/

## Dataset Files

The dataset contains the following CSV files:

- movies.csv
- ratings.csv
- tags.csv
- links.csv

## Download Instructions

1. Open the official MovieLens dataset page.
2. Download the MovieLens 32M dataset.
3. Extract the downloaded ZIP file.
4. Keep the CSV files in the data directory.

## Important Note

The original MovieLens dataset is large. It should not be uploaded directly to GitHub.

Download the dataset locally before running the database import scripts.

The database ETL process uses these CSV files to populate the SQLite database.
