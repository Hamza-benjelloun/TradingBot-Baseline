from .base import Strategy
import pandas as pd
import talib as ta

class RSIStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, rsi_period: int = 14, overbought: int = 70, oversold: int = 30):
        """
        RSI-based strategy implementation.
        :param data: A pandas DataFrame containing OHLC data with at least a 'close' column.
        :param rsi_period: Period for RSI calculation.
        :param overbought: RSI value above which the market is considered overbought.
        :param oversold: RSI value below which the market is considered oversold.
        """
        super().__init__(data)
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold

    def apply_indicators(self):
        """Apply technical indicators to the data."""
        self.data['rsi'] = ta.RSI(self.data['close'], timeperiod=self.rsi_period)

    def generate_signals(self):
        """Generate trading signals based on RSI."""
        self.signals = pd.DataFrame(index=self.data.index)
        self.signals['signal'] = 0.0
        
        # Use .loc to avoid SettingWithCopyWarning
        self.signals.loc[self.data['rsi'] > self.overbought, 'signal'] = -1.0  # Sell signal
        self.signals.loc[self.data['rsi'] < self.oversold, 'signal'] = 1.0   # Buy signal

class StochRSIStrategy(Strategy):
    def __init__(
        self, 
        data: pd.DataFrame, 
        rsi_period: int = 14, 
        stoch_period: int = 14, 
        overbought: float = 80, 
        oversold: float = 20
    ):
        """
        Stochastic RSI-based strategy implementation.
        :param data: A pandas DataFrame containing OHLC data with at least a 'close' column.
        :param rsi_period: Period for RSI calculation.
        :param stoch_period: Period for StochRSI calculation.
        :param overbought: StochRSI %K value above which the market is considered overbought.
        :param oversold: StochRSI %K value below which the market is considered oversold.
        """
        super().__init__(data)
        self.rsi_period = rsi_period
        self.stoch_period = stoch_period
        self.overbought = overbought
        self.oversold = oversold

    def apply_indicators(self):
        """Calculate Stochastic RSI values (%K and %D)."""
        # Calculate RSI
        rsi = ta.RSI(self.data['close'], timeperiod=self.rsi_period)
        
        # Calculate Stochastic RSI
        self.data['stoch_rsi_k'], self.data['stoch_rsi_d'] = ta.STOCH(
            rsi, rsi, rsi, 
            fastk_period=self.stoch_period, 
            slowk_period=3, slowk_matype=0, 
            slowd_period=3, slowd_matype=0
        )

    def generate_signals(self):
        """Generate trading signals based on StochRSI."""
        self.signals = pd.DataFrame(index=self.data.index)
        self.signals['signal'] = 0.0
        
        # Buy when %K is below oversold and crosses above it
        self.signals.loc[self.data['stoch_rsi_k'] < self.oversold, 'signal'] = 1.0
        
        # Sell when %K is above overbought and crosses below it
        self.signals.loc[self.data['stoch_rsi_k'] > self.overbought, 'signal'] = -1.0