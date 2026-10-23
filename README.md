# TVMaze Show Summary

A Python package that downloads TV show records from the TVMaze API, cleans the records, calculates summaries, and writes the results to a JSON file.

## Data source

- API: https://api.tvmaze.com/shows?page=0
- The application retrieves show records from TVMaze.
- An internet connection is required to download records.

## Setup

Create the Conda environment:

```bash
conda env create -f environment.yml
conda activate tvsummary
```

Install the project and its dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

From the project root, run:

```bash
python main.py
```

The application downloads the records and writes the summary to `data/processed/summary.json`.

## Test

Run the offline unit tests:

```bash
python -m unittest discover -s tests
```

The tests check record cleaning and handling of missing values. They do not require an API request.

## Layout

- `main.py` — application entry point
- `src/tvsummary/config.py` — shared configuration
- `src/tvsummary/models.py` — show record model and data cleaning
- `src/tvsummary/sources.py` — TVMaze data retrieval
- `src/tvsummary/aggregations.py` — summary aggregation classes
- `src/tvsummary/report.py` — report generation and JSON output
- `tests/` — offline unit tests
- `data/processed/summary.json` — generated summary

## What moved where

| Lab 02 function or responsibility | Lab 03 location |
|---|---|
| Fetch records from TVMaze | `src/tvsummary/sources.py` |
| Clean and represent individual records | `src/tvsummary/models.py` |
| Count shows by genre | `src/tvsummary/aggregations.py` |
| Calculate average ratings by language | `src/tvsummary/aggregations.py` |
| Count shows by decade | `src/tvsummary/aggregations.py` |
| Combine aggregation results | `src/tvsummary/report.py` |
| Write the JSON summary | `src/tvsummary/report.py` |
| Run the application | `main.py` |
| Store configuration values | `src/tvsummary/config.py` |

## Design choices

- The project uses a `src` package layout and can be installed in editable mode.
- `ShowRecord` cleans malformed or missing values.
- Aggregation subclasses share a common interface, allowing the report to call them without checking their concrete types.
- The TVMaze request logic is isolated in the source module.
- Configuration values are centralized in `config.py`.
- Unit tests use local sample data and do not require a live API connection.

## Known limitations

- Downloading records requires an internet connection and the TVMaze API to be available.
- The summary reflects the records returned by the API when the application runs.
- The current tests cover the record model; they do not test every aggregation or the live network request.
