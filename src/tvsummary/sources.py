"""Download show records from TVMaze."""

import requests

from tvsummary.config import SOURCE_URL, TIMEOUT
from tvsummary.models import ShowRecord


class TVMazeSource:
    """Retrieve and clean show records from the TVMaze API."""

    def __init__(
        self,
        url: str = SOURCE_URL,
        timeout: float = TIMEOUT,
    ) -> None:
        """Set the API URL and request timeout."""
        self.url = url
        self.timeout = timeout

    def fetch_records(self) -> list[ShowRecord]:
        """Download records and return them as ShowRecord objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"Could not download records: {exc}") from exc

        if not isinstance(data, list):
            raise TypeError("Downloaded data is not a list of records.")

        return [ShowRecord(item) for item in data]
