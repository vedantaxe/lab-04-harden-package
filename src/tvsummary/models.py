class ShowRecord:
    """Represent one cleaned TVMaze show record."""

    def __init__(self, data):
        """Create a show record and clean missing or malformed values."""
        data = data if isinstance(data, dict) else {}

        self.name = self._clean_text(data.get("name"))
        self.language = self._clean_text(data.get("language"))
        self.genres = self._clean_genres(data.get("genres"))
        self.premiered = self._clean_date(data.get("premiered"))
        self.rating = self._clean_rating(data.get("rating"))

    @staticmethod
    def _clean_text(value):
        """Return non-empty text or None."""
        return value.strip() if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _clean_genres(value):
        """Return a list containing only non-empty genre strings."""
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    @staticmethod
    def _clean_date(value):
        """Return a valid YYYY-MM-DD-style date string or None."""
        if not isinstance(value, str) or len(value) < 4:
            return None
        if not value[:4].isdigit():
            return None
        return value

    @staticmethod
    def _clean_rating(value):
        """Return a numeric average rating or None."""
        if not isinstance(value, dict):
            return None
        rating = value.get("average")
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            return None
        return rating

    def __str__(self):
        """Return a readable representation of the show."""
        return self.name or "Unknown show"
