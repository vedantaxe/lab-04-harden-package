"""Run the TV summary application."""

import argparse
import json
import logging
import random
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from tvsummary.config import AppConfig, load_config
from tvsummary.errors import ReportError, TVSummaryError
from tvsummary.logging_setup import setup_logging
from tvsummary.models import ShowRecord
from tvsummary.report import SummaryReport
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def select_featured_shows(
    records: list[ShowRecord],
    seed: int,
    sample_size: int,
) -> list[ShowRecord]:
    """Select a reproducible sample of featured shows."""
    return random.Random(seed).sample(
        records,
        k=min(sample_size, len(records)),
    )


def get_tool_version(package_name: str) -> str:
    """Return an installed package version or an unavailable marker."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "not installed"


def write_run_info(config: AppConfig) -> None:
    """Write configuration and environment details beside the summary."""
    run_info = {
        "settings": {
            "source_url": config.source_url,
            "timeout": config.timeout,
            "output_folder": config.output_folder,
            "seed": config.seed,
            "sample_size": config.sample_size,
            "log_level": config.log_level,
        },
        "python_version": sys.version,
        "tool_versions": {
            "pytest": get_tool_version("pytest"),
            "mypy": get_tool_version("mypy"),
            "ruff": get_tool_version("ruff"),
        },
    }

    output_path = Path(config.output_folder) / "run_info.json"
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(run_info, indent=2), encoding="utf-8")
    except OSError as exc:
        raise ReportError(
            f"Could not write run information to '{output_path}'."
        ) from exc


def main(argv: list[str] | None = None) -> int:
    """Run the application and return an exit code."""
    parser = argparse.ArgumentParser(description="Summarize TVMaze show records.")
    parser.add_argument(
        "--config",
        default="config/tvsummary.toml",
        help="Path to the TOML configuration file.",
    )
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        setup_logging(config.log_level)

        logger.info("Starting TV summary application.")
        records = TVMazeSource(config).fetch_records()
        logger.info("Fetched %s show records.", len(records))

        featured_shows = select_featured_shows(
            records,
            seed=config.seed,
            sample_size=config.sample_size,
        )
        logger.info("Selected %s featured shows.", len(featured_shows))

        report = SummaryReport(records)
        summary = report.generate()
        summary["featured_shows"] = [
            {"name": show.name, "language": show.language, "rating": show.rating}
            for show in featured_shows
        ]

        output_path = Path(config.output_folder) / "summary.json"
        report.write(output_path, summary)
        write_run_info(config)
        logger.info("Summary written to %s.", output_path)

        return 0

    except TVSummaryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
