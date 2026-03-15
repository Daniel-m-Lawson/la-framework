"""Provides classes to fetch and transform Binance Kline data into LaKline objects."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from la_framework.la_binance_request import LaBinanceRequest
from la_framework.la_kline import LaKline, LaKlineList


class LaBinanceInterval(str, Enum):
    """Binance API supported kline intervals."""

    SECOND_1 = "1s"
    MINUTE_1 = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"


class LaBinanceRequestKline(LaBinanceRequest):
    """
    Concrete implementation: Fetches and maps Kline data.
    Parameters are provided at call-time, not instantiation.
    """

    # pylint: disable=arguments-differ
    def execute(
        self,
        symbol: str,
        interval: LaBinanceInterval,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 500,
    ) -> LaKlineList:

        # 1. Prepare Parameters
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time:
            params["startTime"] = int(start_time.timestamp() * 1000)
        if end_time:
            params["endTime"] = int(end_time.timestamp() * 1000)

        # 2. Call the base class network helper
        raw_data = self._send_get("/api/v3/klines", params)

        # 3. Transform to LaKlineList
        klines = LaKlineList()
        for item in raw_data:
            k = LaKline(
                ticker=symbol,
                open_time=datetime.fromtimestamp(item[0] / 1000),
                open=Decimal(item[1]),
                high=Decimal(item[2]),
                low=Decimal(item[3]),
                close=Decimal(item[4]),
                volume=Decimal(item[5]),
                close_time=datetime.fromtimestamp(item[6] / 1000),
                quote_volume=Decimal(item[7]),
                trades=int(item[8]),
                taker_base=Decimal(item[9]),
                taker_quote=Decimal(item[10]),
            )
            klines.append(k)

        return klines
