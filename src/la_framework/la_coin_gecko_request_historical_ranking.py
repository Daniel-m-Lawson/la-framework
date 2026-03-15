# la_coin_gecko_request_historical_ranking.py

from decimal import Decimal
from datetime import datetime, timedelta
from typing import cast

from la_framework.la_coin_gecko_request import LaCoinGeckoRequest
from la_framework.la_crypto import LaCrypto, LaCryptoList


class LaCoinGeckoRequestHistoricalRanking(LaCoinGeckoRequest):
    """
    Build historical ranking by market cap for a given date.
    """

    # pylint: disable=arguments-differ
    def execute(self, date: datetime, limit: int = 10) -> LaCryptoList:
        crypto_list = LaCryptoList()

        # 1Get all coin IDs
        all_coins = self._send_get("/coins/list", {})

        start_ts = int((date - timedelta(days=1)).timestamp())
        end_ts = int((date + timedelta(days=1)).timestamp())

        for coin in all_coins:
            try:
                url = f"/coins/{coin['id']}/market_chart/range"
                params = {
                    "vs_currency": "usd",
                    "from": start_ts,
                    "to": end_ts,
                }

                data = self._send_get(url, params)

                if not data["market_caps"]:
                    continue

                market_cap = Decimal(str(data["market_caps"][0][1]))

                crypto = LaCrypto(
                    symbol=coin["symbol"].upper(),
                    name=coin["id"],
                    market_cap=market_cap,
                    circulating_supply=Decimal("0"),
                    price=Decimal("0"),
                )

                crypto_list.append(crypto)

            except Exception:
                continue  # skip broken / delisted coins

        # Rank
        crypto_list.sort_by_market_cap(reverse=True)

        # Return top N
        return cast(LaCryptoList, crypto_list[:limit])
