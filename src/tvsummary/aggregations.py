
"""Aggregation classes for show records."""


class Aggregation:
    """Base class for aggregations."""

    def aggregate(self, records):
        """Calculate a summary from records."""
        raise NotImplementedError("Subclasses must implement aggregate().")


class ShowsPerGenre(Aggregation):
    """Count shows belonging to each genre."""

    key = "shows_per_genre"

    def aggregate(self, records):
        counts = {}

        for show in records:
            for genre in show.genres:
                counts[genre] = counts.get(genre, 0) + 1

        return dict(sorted(counts.items()))


class AverageRatingByLanguage(Aggregation):
    """Calculate average ratings grouped by language."""

    key = "average_rating_by_language"

    def aggregate(self, records):
        ratings = {}

        for show in records:
            if show.language is None or show.rating is None:
                continue

            ratings.setdefault(show.language, []).append(show.rating)

        return {
            language: round(sum(values) / len(values), 2)
            for language, values in sorted(ratings.items())
        }


class ShowsPerDecade(Aggregation):
    """Count shows by premiere decade."""

    key = "shows_per_decade"

    def aggregate(self, records):
        counts = {}

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
