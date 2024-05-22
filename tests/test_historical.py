from src.broker import get_historical_data
from alpaca.data import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from pprint import pprint as print

def test_get_historical_data():
    historical_data = get_historical_data()
    params = StockBarsRequest(
        symbol_or_symbols="SPY",
        start="2021-01-01",
        end="2022-01-01",
        timeframe=TimeFrame.Day,
    )
    data = historical_data.get_stock_bars(params)
    print(data)
    print(type(data))
    assert data is not None