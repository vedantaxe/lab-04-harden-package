
"""Build and write the TVMaze summary report."""

import json
from pathlib import Path

from tvsummary.aggregations import (
    ShowsPerGenre,
    AverageRatingByLanguage,
    ShowsPerDecade,
)


class SummaryReport:
    """Generate and write summaries from show records."""

    def __init__(self, records):
        """Store records and the aggregations to run."""
        self.records = records
        self.aggregations = [
            ShowsPerGenre(),
            AverageRatingByLanguage(),
            ShowsPerDecade(),
        ]

    def generate(self):
        """Run each aggregation through the shared interface."""
        return {
            aggregation.key: aggregation.aggregate(self.records)
            for aggregation in self.aggregations
        }

    def write(self, path, summary):
        """Write the summary dictionary to a JSON file."""
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
