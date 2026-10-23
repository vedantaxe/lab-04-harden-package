"""Tests for the aggregation classes."""

import pytest

from tvsummary.aggregations import (
    AverageRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.models import ShowRecord


def test_shows_per_genre(sample_records: list[ShowRecord]) -> None:
    """Count genres across all records."""
    result = ShowsPerGenre().aggregate(sample_records)

    assert result == {"Anime": 1, "Crime": 1, "Drama": 2}


def test_average_rating_by_language(
    sample_records: list[ShowRecord],
) -> None:
    """Calculate average ratings and skip missing values."""
    result = AverageRatingByLanguage().aggregate(sample_records)

    assert result == {"English": 7.0, "Japanese": 9.0}


def test_shows_per_decade(sample_records: list[ShowRecord]) -> None:
    """Count shows by premiere decade."""
    result = ShowsPerDecade().aggregate(sample_records)

    assert result == {1990: 2, 2000: 1}


@pytest.mark.parametrize(
    ("genres", "expected"),
    [
        (["Drama", "Drama"], {"Drama": 2}),
        ([], {}),
        (["Comedy"], {"Comedy": 1}),
    ],
)
def test_shows_per_genre_parametrized(
    genres: list[str],
    expected: dict[str, int],
) -> None:
    """Test genre aggregation against several inputs."""
    record = ShowRecord({"genres": genres})

    assert ShowsPerGenre().aggregate([record]) == expected
