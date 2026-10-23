"""Download show records from TVMaze."""

import requests

from tvsummary.config import AppConfig
from tvsummary.errors import DataSourceError, DataValidationError
from tvsummary.models import ShowRecord


class TVMazeSource:
    """Retrieve and clean show records from the TVMaze API."""

    def __init__(self, config: AppConfig) -> None:
        """Set the API URL and request timeout from configuration."""
        self.url = config.source_url
        self.timeout = config.timeout

    def fetch_records(self) -> list[ShowRecord]:
        """Download records and return them as ShowRecord objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise DataSourceError(f"Could not download records: {exc}") from exc
        except ValueError as exc:
            raise DataSourceError("TVMaze returned invalid JSON.") from exc

        if not isinstance(data, list):
            raise DataValidationError("Downloaded data is not a list of records.")

        try:
            return [ShowRecord(item) for item in data]
        except (TypeError, ValueError, KeyError) as exc:
            raise DataValidationError(
                "Downloaded records contain invalid data."
            ) from exc
