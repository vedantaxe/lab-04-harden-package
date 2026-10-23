"""Configure application logging."""

import logging


def setup_logging(level: str) -> None:
    """Configure the root logger using the requested logging level."""
    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(numeric_level, int):
        raise TypeError(f"Invalid logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
