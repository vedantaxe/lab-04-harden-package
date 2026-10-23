"""Tests for TOML configuration loading and validation."""

import pytest

from tvsummary.config import AppConfig, load_config
from tvsummary.errors import ConfigurationError


def test_load_valid_config(tmp_path) -> None:
    """Load valid settings from a temporary TOML file."""
    config_file = tmp_path / "settings.toml"
    config_file.write_text(
        'source_url = "https://example.com/shows"\n'
        "timeout = 5\n"
        'output_folder = "output"\n'
        "seed = 42\n"
        "sample_size = 10\n"
        'log_level = "INFO"\n',
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert isinstance(config, AppConfig)
    assert config.source_url == "https://example.com/shows"
    assert config.timeout == 5.0
    assert config.output_folder == "output"
    assert config.seed == 42
    assert config.sample_size == 10
    assert config.log_level == "INFO"


def test_missing_config_file_raises_error(tmp_path) -> None:
    """Raise a custom error when the file does not exist."""
    with pytest.raises(ConfigurationError, match="Could not load"):
        load_config(tmp_path / "missing.toml")


def test_missing_setting_raises_error(tmp_path) -> None:
    """Raise a custom error when a required setting is missing."""
    config_file = tmp_path / "incomplete.toml"
    config_file.write_text(
        'source_url = "https://example.com/shows"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="Missing configuration setting"):
        load_config(config_file)


def test_invalid_timeout_raises_error(tmp_path) -> None:
    """Reject a timeout that is not positive."""
    config_file = tmp_path / "bad-timeout.toml"
    config_file.write_text(
        'source_url = "https://example.com/shows"\n'
        "timeout = 0\n"
        'output_folder = "output"\n'
        "seed = 42\n"
        "sample_size = 10\n"
        'log_level = "INFO"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="timeout must be a positive number"):
        load_config(config_file)


def test_invalid_toml_raises_error(tmp_path) -> None:
    """Reject malformed TOML syntax."""
    config_file = tmp_path / "malformed.toml"
    config_file.write_text("timeout = [\n", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Could not load"):
        load_config(config_file)
