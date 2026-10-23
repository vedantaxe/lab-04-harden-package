"""Public interface for the tvsummary package."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.models import ShowRecord
from tvsummary.report import SummaryReport
from tvsummary.sources import TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "ShowRecord",
    "ShowsPerDecade",
    "ShowsPerGenre",
    "SummaryReport",
    "TVMazeSource",
]
