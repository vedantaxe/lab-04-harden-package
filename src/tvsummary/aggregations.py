"""Aggregation classes for show records."""

from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar

from tvsummary.models import ShowRecord

ResultT = TypeVar("ResultT")


class Aggregation(ABC, Generic[ResultT]):
    """Base class for aggregations."""

    key: ClassVar[str]

    @abstractmethod
    def aggregate(self, records: list[ShowRecord]) -> ResultT:
        """Calculate a summary from records."""
        raise NotImplementedError("Subclasses must implement aggregate().")


class ShowsPerGenre(Aggregation[dict[str, int]]):
    """Count shows belonging to each genre."""

    key = "shows_per_genre"

    def aggregate(self, records: list[ShowRecord]) -> dict[str, int]:
        counts: dict[str, int] = {}

        for show in records:
            for genre in show.genres:
                counts[genre] = counts.get(genre, 0) + 1

        return dict(sorted(counts.items()))


class AverageRatingByLanguage(Aggregation[dict[str, float]]):
    """Calculate average ratings grouped by language."""

    key = "average_rating_by_language"

    def aggregate(self, records: list[ShowRecord]) -> dict[str, float]:
        ratings: dict[str, list[int | float]] = {}

        for show in records:
            if show.language is None or show.rating is None:
                continue

            ratings.setdefault(show.language, []).append(show.rating)

        return {
            language: round(sum(values) / len(values), 2)
            for language, values in sorted(ratings.items())
        }


class ShowsPerDecade(Aggregation[dict[int, int]]):
    """Count shows by premiere decade."""

    key = "shows_per_decade"

    def aggregate(self, records: list[ShowRecord]) -> dict[int, int]:
        counts: dict[int, int] = {}

        for show in records:
            if show.premiered is None:
                continue

            try:
                year = int(show.premiered[:4])
            except ValueError:
                continue

            decade = (year // 10) * 10
            counts[decade] = counts.get(decade, 0) + 1

        return dict(sorted(counts.items()))
