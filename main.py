
"""Run the TVMaze summary application."""

from tvsummary.config import OUTPUT_PATH
from tvsummary.report import SummaryReport
from tvsummary.sources import TVMazeSource


def main():
    """Download records, generate a report, and save the JSON output."""
    try:
        source = TVMazeSource()
        records = source.fetch_records()

        if len(records) < 50:
            raise RuntimeError(
                f"Expected at least 50 records, but received {len(records)}."
            )

        report = SummaryReport(records)
        summary = {
            "source_url": source.url,
            "record_count": len(records),
            **report.generate(),
        }

        report.write(OUTPUT_PATH, summary)

        print(f"Downloaded {len(records)} records.")
        print(f"Summary written to {OUTPUT_PATH}.")

    except (RuntimeError, OSError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
