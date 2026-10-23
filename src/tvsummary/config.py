"""Load and validate application settings from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from tvsummary.errors import ConfigurationError


@dataclass(frozen=True)
class AppConfig:
    """Store immutable application settings."""

    source_url: str
    timeout: float
    output_folder: str
    seed: int
    sample_size: int
    log_level: str


def load_config(path: str | Path) -> AppConfig:
    """Load settings from a TOML file and validate their values."""
    config_path = Path(path)

    try:
        with config_path.open("rb") as file:
            data = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(
            f"Could not load configuration file '{config_path}'."
        ) from exc

    try:
        source_url = data["source_url"]
        timeout = data["timeout"]
        output_folder = data["output_folder"]
        seed = data["seed"]
        sample_size = data["sample_size"]
        log_level = data["log_level"]
    except KeyError as exc:
        raise ConfigurationError(
            f"Missing configuration setting: {exc.args[0]}"
        ) from exc

    if not isinstance(source_url, str) or not source_url.strip():
        raise ConfigurationError("source_url must be a non-empty string.")

    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ConfigurationError("timeout must be a positive number.")

    if not isinstance(output_folder, str) or not output_folder.strip():
        raise ConfigurationError("output_folder must be a non-empty string.")

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ConfigurationError("seed must be an integer.")

    if (
        isinstance(sample_size, bool)
        or not isinstance(sample_size, int)
        or sample_size < 1
    ):
        raise ConfigurationError("sample_size must be a positive integer.")

    if not isinstance(log_level, str) or log_level.upper() not in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
    }:
        raise ConfigurationError("log_level must be DEBUG, INFO, WARNING, or ERROR.")

    return AppConfig(
        source_url=source_url,
        timeout=float(timeout),
        output_folder=output_folder,
        seed=seed,
        sample_size=sample_size,
        log_level=log_level.upper(),
    )
