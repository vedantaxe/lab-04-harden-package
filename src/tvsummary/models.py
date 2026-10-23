"""Represent cleaned TVMaze show records."""

from typing import Any


class ShowRecord:
    """Represent one cleaned TVMaze show record."""

    name: str | None
    language: str | None
    genres: list[str]
    premiered: str | None
    rating: int | float | None

    def __init__(self, data: object) -> None:
        """Create a show record and clean missing or malformed values."""
        raw: dict[str, Any] = data if isinstance(data, dict) else {}

        self.name = self._clean_text(raw.get("name"))
        self.language = self._clean_text(raw.get("language"))
        self.genres = self._clean_genres(raw.get("genres"))
        self.premiered = self._clean_date(raw.get("premiered"))
        self.rating = self._clean_rating(raw.get("rating"))

    @staticmethod
    def _clean_text(value: object) -> str | None:
        """Return non-empty text or None."""
        return value.strip() if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _clean_genres(value: object) -> list[str]:
        """Return a list containing only non-empty genre strings."""
        if not isinstance(value, list):
            return []
        return [
            item.strip() for item in value if isinstance(item, str) and item.strip()
        ]

    @staticmethod
    def _clean_date(value: object) -> str | None:
        """Return a valid YYYY-MM-DD-style date string or None."""
        if not isinstance(value, str) or len(value) < 4:
            return None
        if not value[:4].isdigit():
            return None
        return value

    @staticmethod
    def _clean_rating(value: object) -> int | float | None:
        """Return a numeric average rating or None."""
        if not isinstance(value, dict):
            return None
        rating = value.get("average")
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            return None
        return rating

    def __str__(self) -> str:
        """Return a readable representation of the show."""
        return self.name or "Unknown show"
