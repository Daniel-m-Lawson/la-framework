from abc import ABC, abstractmethod
from typing import Any
import requests


class LaCoinGeckoRequest(ABC):
    """Abstract base class for all CoinGecko API requests."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.session = requests.Session()

    def _send_get(self, endpoint: str, params: dict) -> Any:
        """Helper to perform GET request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Subclasses must implement execution and transformation logic."""
