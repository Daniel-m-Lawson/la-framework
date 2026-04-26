from dataclasses import dataclass
from decimal import Decimal

from .la_keyed_class import LaKeyedClass
from .la_list import LaList


@dataclass
class LaCrypto(LaKeyedClass):
    """
    Represents a cryptocurrency with market data.
    """

    symbol: str
    name: str
    market_cap: Decimal
    circulating_supply: Decimal
    price: Decimal

    @property
    def key(self) -> str:
        return self.symbol


class LaCryptoList(LaList[LaCrypto]):
    """Type-safe list of LaCrypto objects."""

    def total_market_cap(self):
        return sum(c.market_cap for c in self._items)

    def to_market_cap_distribution(self, percentage: bool = False):
        total = self.total_market_cap()

        if percentage:
            return {c.symbol: float(c.market_cap / total * 100) for c in self._items}

        return {c.symbol: float(c.market_cap) for c in self._items}

    def sort_by_market_cap(self, reverse=True):
        super().sort(key=lambda c: c.market_cap, reverse=reverse)
