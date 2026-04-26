from datetime import datetime
from decimal import Decimal
from .la_coin_gecko_request import LaCoinGeckoRequest
from ..core import LaCrypto


class LaCoinGeckoRequestHistoricalMarketCap(LaCoinGeckoRequest):
    """
    Fetch historical market cap for a single coin on a specific date.
    """

    def execute(self, coin_id: str, date: datetime) -> LaCrypto:

        formatted_date = date.strftime("%d-%m-%Y")
        url = f"/coins/{coin_id}/history"
        params = {"date": formatted_date, "localization": "false"}

        raw = self._send_get(url, params)
        market_data = raw.get("market_data", {})

        return LaCrypto(
            symbol=raw["symbol"].upper(),
            name=raw["name"],
            market_cap=Decimal(str(market_data.get("market_cap", {}).get("usd", 0))),
            circulating_supply=Decimal("0"),  # Not available historically
            price=Decimal(str(market_data.get("current_price", {}).get("usd", 0))),
        )
