from client import get_historical_data
from alpaca.data import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from pandas import DataFrame


def test_get_historical_data():
    historical_data = get_historical_data()
    params = StockBarsRequest(
        symbol_or_symbols="SPY",
        start="2021-01-01",
        end="2022-01-01",
        timeframe=TimeFrame.Day,
    )
    bars = historical_data.get_stock_bars(params).df
    assert isinstance(bars, DataFrame)
    assert bars.shape[0] == 252
    assert (
        bars.columns
        == ["open", "high", "low", "close", "volume", "trade_count", "vwap"]
    ).all()
