from client import get_historical_data
from alpaca.data import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import datetime
from pandas import DataFrame


def test_broker():
    broker = get_historical_data()
    bars = broker.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols="AAPL",
            timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
            limit=100,
            start=datetime.datetime(2021, 2, 11),
            end=datetime.datetime(2024, 2, 11),
        )
    ).df
    assert isinstance(bars, DataFrame)
    assert bars.shape[0] == 100
    assert (
        bars.columns
        == ["open", "high", "low", "close", "volume", "trade_count", "vwap"]
    ).all()
