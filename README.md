# TVMaze Show Summary

A typed Python package that retrieves TV show records from the TVMaze API, validates and cleans the data, calculates summaries, selects featured shows reproducibly, and writes JSON reports.

## Data source

- API: `https://api.tvmaze.com/shows?page=0`
- An internet connection is required to download show records.
- Unit tests use local sample data and do not require network access.

## Setup

Create and activate the Conda environment:

```powershell
conda env create -f environment.yml
conda activate tvsummary-lab04
```

Install the pinned dependencies and the package in editable mode:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

From the project root:

```powershell
python -m tvsummary.main
```

To specify a configuration file:

```powershell
python -m tvsummary.main --config config/tvsummary.toml
```

The default configuration is `config/tvsummary.toml`. It controls the source URL, request timeout, output folder, random seed, featured-show sample size, and logging level.

The application writes:

- `data/processed/summary.json` — aggregation results and featured shows.
- `data/processed/run_info.json` — configuration settings, Python version, and pytest, mypy, and Ruff versions.

## Check it

Run these checks from the project root:

```powershell
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

The tests run offline and use sample records or temporary files. They do not require a live TVMaze request.

## Errors and exit codes

- Exit code `0`: the application completed successfully.
- Exit code `1`: an expected application error occurred. The application prints an `Error:` message to standard error.
- Configuration, data-source, data-validation, and report-writing failures use custom package exceptions.
- Unexpected programming errors are not silently swallowed.

## Reproducing a run

1. Use the same Python environment and dependency versions.
2. Keep the same `config/tvsummary.toml` settings.
3. Keep the same `seed` and `sample_size` to reproduce featured-show selection for the same input records.
4. Run `python -m tvsummary.main`.
5. Inspect `data/processed/summary.json` and `data/processed/run_info.json`.

The featured-show selection is reproducible when the input records, seed, and sample size remain the same. The complete summary can change when the TVMaze API data changes.

## Project layout

- `src/tvsummary/__init__.py` — package initialization
- `src/tvsummary/config.py` — TOML configuration loading and validation
- `src/tvsummary/errors.py` — custom package exceptions
- `src/tvsummary/logging_setup.py` — logging configuration
- `src/tvsummary/models.py` — show record model and data cleaning
- `src/tvsummary/sources.py` — TVMaze data retrieval
- `src/tvsummary/aggregations.py` — summary aggregation classes
- `src/tvsummary/report.py` — aggregation results and JSON report writing
- `src/tvsummary/main.py` — application entry point
- `config/tvsummary.toml` — application settings
- `tests/` — offline tests
- `data/processed/` — generated JSON output

## Known limitations

- Downloading records requires an internet connection and TVMaze availability.
- Summary values reflect the records returned by the API at run time.
- Reproducible featured-show selection does not guarantee identical summaries if the API data changes.
