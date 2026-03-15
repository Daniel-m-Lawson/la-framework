# la_coin_gecko_request_market_cap.py
from decimal import Decimal
from la_framework.la_coin_gecko_request import LaCoinGeckoRequest
from la_framework.la_crypto import LaCrypto, LaCryptoList


class LaCoinGeckoRequestMarketCap(LaCoinGeckoRequest):
    """
    Fetch top cryptocurrencies by market cap from CoinGecko.
    """

    def execute(self, limit: int = 100) -> LaCryptoList:
        url = "/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
        }

        raw_data = self._send_get(url, params)
        crypto_list = LaCryptoList()

        for coin in raw_data:
            crypto = LaCrypto(
                symbol=coin["symbol"].upper(),
                name=coin["name"],
                market_cap=Decimal(str(coin["market_cap"])),
                circulating_supply=Decimal(str(coin.get("circulating_supply") or 0)),
                price=Decimal(str(coin["current_price"])),
            )
            crypto_list.append(crypto)

        return crypto_list
