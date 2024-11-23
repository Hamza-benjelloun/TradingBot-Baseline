from src.strategies.main import Strategy
from src.strategies.rsi import RSIStrategy
from src.broker import get_trading_client
import pandas as pd
import pytest


@pytest.fixture
def strategy():
    data = pd.DataFrame(
        {
            "Open": [10, 11, 12, 13, 14],
            "High": [15, 16, 17, 18, 19],
            "Low": [8, 9, 10, 11, 12],
            "Close": [14, 15, 16, 17, 18],
            "Volume": [1000, 2000, 3000, 4000, 5000],
        }
    )
    return Strategy(data)


@pytest.fixture
def rsi_strategy(broker):
    data = broker.get_bars(
        symbol="AAPL",
        timeframe="1Min",
        limit=100,
    ).df
    return RSIStrategy(data)


@pytest.fixture
def broker():
    return get_trading_client()


def test_main(strategy):
    assert not strategy.signals.empty


def test_rsi(rsi_strategy):
    rsi_strategy.apply_indicators()
    rsi_strategy.generate_signals()
    print(rsi_strategy.signals.describe())
    assert (rsi_strategy.signals["signal"] == -1.0).any() or (
        rsi_strategy.signals["signal"] == 1
    ).any()
    assert rsi_strategy.data["rsi"].notnull().any()
