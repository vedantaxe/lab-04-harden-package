"""Build and write the TVMaze summary report."""

import json
from pathlib import Path
from typing import Any

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.errors import ReportError
from tvsummary.models import ShowRecord


class SummaryReport:
    """Generate and write summaries from show records."""

    def __init__(self, records: list[ShowRecord]) -> None:
        """Store records and the aggregations to run."""
        self.records = records
        self.aggregations: list[Aggregation[Any]] = [
            ShowsPerGenre(),
            AverageRatingByLanguage(),
            ShowsPerDecade(),
        ]

    def generate(self) -> dict[str, Any]:
        """Run each aggregation through the shared interface."""
        return {
            aggregation.key: aggregation.aggregate(self.records)
            for aggregation in self.aggregations
        }

    def write(self, path: str | Path, summary: dict[str, Any]) -> None:
        """Write the summary dictionary to a JSON file."""
        output = Path(path)
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        except OSError as exc:
            raise ReportError(f"Could not write report to '{output}'.") from exc
