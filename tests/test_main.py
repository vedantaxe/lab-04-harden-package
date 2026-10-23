"""Tests for the application entry point."""

from tvsummary.main import main, select_featured_shows
from tvsummary.models import ShowRecord


def test_main_reports_configuration_failure(capsys, tmp_path) -> None:
    """Return one and print an error when configuration is missing."""
    missing_config = tmp_path / "missing.toml"

    exit_code = main(["--config", str(missing_config)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.err.startswith("Error:")
    assert "Traceback" not in captured.err
    assert captured.out == ""


def test_main_success(monkeypatch, tmp_path) -> None:
    """Return zero and write a report when processing succeeds."""
    config_file = tmp_path / "settings.toml"
    config_file.write_text(
        f'source_url = "https://example.com/shows"\n'
        f"timeout = 5\n"
        f'output_folder = "{tmp_path.as_posix()}"\n'
        f"seed = 42\n"
        f"sample_size = 2\n"
        f'log_level = "ERROR"\n',
        encoding="utf-8",
    )

    class FakeSource:
        def __init__(self, config) -> None:
            pass

        def fetch_records(self):
            from tvsummary.models import ShowRecord

            return [
                ShowRecord(
                    {
                        "name": "Test Show",
                        "language": "English",
                        "genres": ["Drama"],
                        "premiered": "2020-01-01",
                        "rating": {"average": 8.0},
                    }
                )
            ]

    monkeypatch.setattr("tvsummary.main.TVMazeSource", FakeSource)

    exit_code = main(["--config", str(config_file)])

    assert exit_code == 0
    assert (tmp_path / "summary.json").exists()


def test_featured_show_selection_is_reproducible() -> None:
    """The same seed selects the same featured shows."""
    records = [ShowRecord({"name": f"Show {number}"}) for number in range(10)]

    first = select_featured_shows(records, seed=42, sample_size=4)
    second = select_featured_shows(records, seed=42, sample_size=4)

    assert [show.name for show in first] == [show.name for show in second]
    assert len(first) == 4
