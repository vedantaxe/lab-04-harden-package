
"""Tests for the ShowRecord model."""

import unittest

from tvsummary.models import ShowRecord


class TestShowRecord(unittest.TestCase):
    """Test show record cleaning and string representation."""

    def test_cleans_valid_record(self):
        """Clean whitespace and invalid genre entries."""
        show = ShowRecord({
            "name": "  Demo Show  ",
            "language": " English ",
            "genres": ["Drama", None, "", " Comedy "],
            "premiered": "2020-01-15",
            "rating": {"average": 8.2},
        })

        self.assertEqual(show.name, "Demo Show")
        self.assertEqual(show.language, "English")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.rating, 8.2)
        self.assertEqual(str(show), "Demo Show")

    def test_handles_missing_values(self):
        """Handle an empty record without crashing."""
        show = ShowRecord({})

        self.assertEqual(str(show), "Unknown show")
        self.assertIsNone(show.name)
        self.assertIsNone(show.language)
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)


if __name__ == "__main__":
    unittest.main()
