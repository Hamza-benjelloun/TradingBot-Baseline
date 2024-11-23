import pandas as pd

class Strategy:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the strategy with historical market data.

        :param data: A DataFrame containing the historical price data.
                     It should include at least the columns: 'Open', 'High', 'Low', 'Close', 'Volume'.
        """
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.signals['signal'] = 0.0

    def apply_indicators(self):
        """
        Apply technical indicators to the data.
        This method should be overridden by subclasses to add custom indicators.
        Example:
            self.data['rsi'] = talib.RSI(self.data['Close'])
        """
        raise NotImplementedError("Should implement apply_indicators()")

    def generate_signals(self):
        """
        Generate trading signals based on the applied indicators.
        This method should be overridden by subclasses to generate specific signals.
        Example:
            self.signals['signal'] = np.where(self.data['rsi'] > 70, -1.0, 0.0)
        """
        raise NotImplementedError("Should implement generate_signals()")

    def get_signals(self):
        """
        Get the generated signals.

        :return: A DataFrame containing the signals.
        """
        return self.signals