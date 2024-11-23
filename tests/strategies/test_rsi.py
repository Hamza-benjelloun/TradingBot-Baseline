from src.strategies.rsi import RSIStrategy
import pandas as pd
import numpy as np


def test_rsi_strategy():
    mock_data = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    })

    rsi_strategy = RSIStrategy(data=mock_data, rsi_period=3, overbought=70, oversold=30)

    rsi_strategy.apply_indicators()
    rsi_strategy.generate_signals()

    valid_rsi = rsi_strategy.data['rsi'].dropna()
    valid_signals = rsi_strategy.signals.loc[valid_rsi.index, 'signal']

    # Assert RSI column is present
    assert 'rsi' in rsi_strategy.data.columns, "RSI column not calculated"

    # Assert RSI values are numeric and non-NaN for valid rows
    assert valid_rsi.notnull().all(), "RSI contains unexpected NaN values after valid period"

    # Assert signals are generated correctly
    expected_signals = []
    for rsi_value in valid_rsi:
        if rsi_value < rsi_strategy.oversold:
            expected_signals.append(1.0)  # Buy signal
        elif rsi_value > rsi_strategy.overbought:
            expected_signals.append(-1.0)  # Sell signal
        else:
            expected_signals.append(0.0)  # No signal

    # Compare the generated signals with the expected ones
    actual_signals = valid_signals.values
    assert np.array_equal(actual_signals, expected_signals), (
        f"Expected signals {expected_signals}, but got {list(actual_signals)}"
    )