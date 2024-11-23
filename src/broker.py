from alpaca.trading.client import TradingClient
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
import yaml


broker_config = yaml.safe_load(open("config.yaml", "r"))["broker"]

API_KEY = broker_config.get("API_KEY")
API_SECRET = broker_config.get("API_SECRET")
BASE_URL = broker_config.get("BASE_URL")
IS_PAPER = broker_config.get("PAPER", True)

assert API_KEY is not None, "API_KEY is missing in broker_config"
assert API_SECRET is not None, "API_SECRET is missing in broker_config"
assert BASE_URL is not None, "BASE_URL is missing in broker_config"

ALPACA_CREDS = {"api_key": API_KEY, "secret_key": API_SECRET, "paper": IS_PAPER}


def get_trading_client():
    return TradingClient(**ALPACA_CREDS)


def get_streamer():
    return StockDataStream(
        api_key=API_KEY,
        secret_key=API_SECRET,
    )


def get_historical_data():
    return StockHistoricalDataClient(
        api_key=API_KEY,
        secret_key=API_SECRET,
    )