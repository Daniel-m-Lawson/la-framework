from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from la_framework.la_keyed_class import LaKeyedClass
from la_framework.la_list import LaList


@dataclass
class LaKline(LaKeyedClass):
    """Represents a single candlestick (kline) data point for a financial instrument."""

    ticker: str
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    close_time: datetime
    quote_volume: Decimal | None = None
    trades: int | None = None
    taker_base: Decimal | None = None
    taker_quote: Decimal | None = None

    @property
    def key(self) -> tuple[str, datetime, datetime]:
        return (self.ticker, self.open_time, self.close_time)


class LaKlineList(LaList[LaKline]):
    """A type-safe list of LaKline objects with O(1) key-based lookups."""

    def get_kline(
        self, ticker: str, open_time: datetime, close_time: datetime
    ) -> LaKline:
        return self.get((ticker, open_time, close_time))

    def normalise(self, base_value: float = 1.0) -> "LaKlineList":
        """
        Rescales all OHLC values based on the first candle's open price.
        If first open is 100, and we normalise to base 1.0, 100 becomes 1.0.
        """
        if not self._items:
            return self

        # 1. Get the divisor from the first candle's open
        first_open = self._items[0].open
        # We convert the base_value to Decimal to match your LaKline types
        multiplier = Decimal(str(base_value)) / first_open

        normalised_list = LaKlineList()

        for kline in self._items:
            # Create a copy so we don't modify the original data
            new_kline = deepcopy(kline)

            # 2. Rescale all price-based attributes
            new_kline.open *= multiplier
            new_kline.high *= multiplier
            new_kline.low *= multiplier
            new_kline.close *= multiplier
            # We typically don't normalise volume unless requested

            normalised_list.append(new_kline)

        return normalised_list
