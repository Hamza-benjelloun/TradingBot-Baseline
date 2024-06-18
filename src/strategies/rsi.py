# Example subclass implementing a simple RSI-based strategy
from .main import Strategy
import talib
import pandas as pd


class RSIStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, rsi_period: int = 14, overbought: int = 70, oversold: int = 30):
        super().__init__(data)
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold

    def apply_indicators(self):
        self.data['rsi'] = talib.RSI(self.data['Close'], timeperiod=self.rsi_period)

    def generate_signals(self):
        self.signals['signal'] = 0.0
        self.signals['signal'][self.data['rsi'] > self.overbought] = -1.0
        self.signals['signal'][self.data['rsi'] < self.oversold] = 1.0