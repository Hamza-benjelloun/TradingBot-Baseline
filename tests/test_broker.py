from src.broker import init_rest_client

def test_broker():
    broker = init_rest_client()
    bars = broker.get_bars(
        symbol="AAPL",
        timeframe="1Min",
        limit=100,
    ).df
    print(bars.describe())