import talib
import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the strategy with historical market data.

        :param data: A DataFrame containing the historical price data.
        """
        self.data = data
        self.signals = pd.DataFrame(index=data.index)
        self.signals['signal'] = 0.0

    def apply_indicators(self):
        """
        Apply technical indicators to the data.
        This method should be overridden by subclasses to add custom indicators.
        # Example:
        # self.data['rsi'] = talib.RSI(self.data['Close'])
        """
        raise NotImplementedError("Should implement apply_indicators()")

    def generate_signals(self):
        """
        Generate trading signals based on the applied indicators.
        This method should be overridden by subclasses to generate specific signals.
        # Example:
        # self.signals['signal'] = np.where(self.data['rsi'] > 70, -1.0, 0.0)
        """
        raise NotImplementedError("Should implement generate_signals()")

    def get_signals(self):
        """
        Get the generated signals.

        :return: A DataFrame containing the signals.
        """
        return self.signals

# Example of a specific strategy inheriting from the Strategy base class SMA (update the code)
class MovingAverageCrossStrategy(Strategy):
    def __init__(self, data, short_window=9, long_window=50):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window

    def apply_indicators(self):
        """
        Apply moving average indicators to the data.
        """
        self.data['short_mavg'] = talib.SMA(self.data['Close'], timeperiod=self.short_window)
        self.data['long_mavg'] = talib.SMA(self.data['Close'], timeperiod=self.long_window)

    def generate_signals(self):
        """
        Generate buy/sell signals based on moving average cross strategy.
        """
        self.apply_indicators()
        self.signals['signal'] = 0.0
        self.signals['signal'][self.short_window:] = \
            np.where(self.data['short_mavg'][self.short_window:] > self.data['long_mavg'][self.short_window:], 1.0, 0.0)

        return self.signals