from abc import ABC, abstractmethod
from typing import Any
import requests


class LaBinanceRequest(ABC):
    """Abstract base class for all Binance API requests."""

    BASE_URL = "https://api.binance.com"

    def __init__(self):
        # We initialize the session once to benefit from connection pooling
        self.session = requests.Session()

    def _send_get(self, endpoint: str, params: dict) -> Any:
        """Helper to handle the actual HTTP GET request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Subclasses must implement the execution and transformation logic."""
