"""Shared fixtures for the test suite."""

import pytest

from tvsummary.models import ShowRecord


@pytest.fixture
def sample_records() -> list[ShowRecord]:
    """Provide sample records without making network requests."""
    return [
        ShowRecord(
            {
                "name": "Drama One",
                "language": "English",
                "genres": ["Drama", "Crime"],
                "premiered": "1995-01-01",
                "rating": {"average": 8.0},
            }
        ),
        ShowRecord(
            {
                "name": "Drama Two",
                "language": "English",
                "genres": ["Drama"],
                "premiered": "2005-01-01",
                "rating": {"average": 6.0},
            }
        ),
        ShowRecord(
            {
                "name": "Anime One",
                "language": "Japanese",
                "genres": ["Anime"],
                "premiered": "1999-05-01",
                "rating": {"average": 9.0},
            }
        ),
        ShowRecord(
            {
                "name": "Missing Data",
                "genres": [],
            }
        ),
    ]
