"""Public interface for the tvsummary package."""

from tvsummary.models import ShowRecord
from tvsummary.sources import TVMazeSource
from tvsummary.aggregations import (
    Aggregation,
    ShowsPerGenre,
    AverageRatingByLanguage,
    ShowsPerDecade,
)
from tvsummary.report import SummaryReport

__all__ = [
    "ShowRecord",
    "TVMazeSource",
    "Aggregation",
    "ShowsPerGenre",
    "AverageRatingByLanguage",
    "ShowsPerDecade",
    "SummaryReport",
]