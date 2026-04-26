# la-framework

Daniel's internal Python framework — a standard library shared across personal projects.

## Installation

```bash
pip install -e .
```

Or install from a built wheel:

```bash
pip install dist/la_framework-0.1.0-py3-none-any.whl
```

## Modules

| Class | Module | Description |
|---|---|---|
| `LaKeyedClass` | `la_keyed_class` | Abstract base for objects with a key |
| `LaList` | `la_list` | Generic typed list with filtering/lookup helpers |
| `LaKline`, `LaKlineList` | `la_kline` | OHLCV candlestick data structures |
| `LaBinanceRequest` | `la_binance_request` | Base class for Binance API requests |
| `LaBinanceRequestKline`, `LaBinanceInterval` | `la_binance_request_kline` | Fetch kline data from Binance |
| `LaPlotKline`, `LaPlotPie`, `LaPlotTimeSeries` | `la_plot` | Plotly chart helpers |
| `LaCrypto`, `LaCryptoList` | `la_crypto` | Cryptocurrency data structures |
| `LaCoinGeckoRequest` | `la_coin_gecko_request` | Base class for CoinGecko API requests |
| `LaCoinGeckoRequestMarketCap` | `la_coin_gecko_request_market_cap` | Fetch current market cap data |
| `LaCoinGeckoRequestHistoricalMarketCap` | `la_coin_gecko_request_historical_market_cap` | Fetch historical market cap data |
| `LaCoinGeckoRequestHistoricalRanking` | `la_coin_gecko_request_historical_ranking` | Fetch historical ranking data |
| `LaDatabase` | `la_database` | SQL Server database connection wrapper (pyodbc) |
| `LaTable` | `la_table` | Generic dataclass-to-database-table helper |

## Dependencies

- `pyodbc>=4.0` — SQL Server database connectivity
- `requests>=2.28` — HTTP requests (Binance, CoinGecko APIs)
- `plotly>=5.0` — Interactive charts

## Development

Create a virtual environment and install in editable mode:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Build a distributable wheel:

```bash
pip install build
python -m build
```
