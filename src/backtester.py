import pandas as pd

from src.strategies.base import Strategy
from src.trader import Trader


class Backtester:
    def __init__(
        self,
        strategy: Strategy,
        trader: Trader,
        initial_capital=100000,
        risk_tolerance=0.02,
        take_profit=0.05,
        stop_loss=0.02,
        max_positions=10,
    ):
        """
        Backtest a strategy using a Trader object.

        :param strategy: The strategy to backtest (RSIStrategy, StochRSIStrategy, etc.).
        :param trader: The Trader object to simulate trades.
        :param initial_capital: Initial capital for the backtest.
        :param risk_tolerance: Risk tolerance for the trader.
        :param max_positions: Maximum number of positions allowed in the portfolio.
        """
        self.strategy = strategy
        self.trader = trader
        trader.initial_capital = initial_capital
        trader.risk_tolerance = risk_tolerance
        trader.max_positions = max_positions
        trader.stop_loss = stop_loss
        trader.take_profit = take_profit
        self.results = []

    def run(self):
        """
        Run the backtest by applying the strategy to historical data.
        """
        self.strategy.apply_indicators()
        self.strategy.generate_signals()

        for i, row in self.strategy.signals.iterrows():
            signal = row["signal"]
            if signal == 1:
                # Buy signal
                self.trader.execute_trade(
                    signal,
                    self.strategy.data["ticker"][i],
                    self.strategy.data["close"][i],
                    self.strategy.data["close"][i] * (1 - self.trader.stop_loss),
                )
            elif signal == -1:
                # Sell signal
                self.trader.execute_trade(
                    signal,
                    self.strategy.data["ticker"][i],
                    self.strategy.data["close"][i],
                    self.strategy.data["close"][i] * (1 + self.trader.take_profit),
                )

            # Log portfolio value
            portfolio_value = self.trader.calculate_portfolio_value()
            self.results.append(
                {
                    "date": i,
                    "portfolio_value": portfolio_value,
                    "cash": self.trader.cash,
                    "portfolio": self.trader.portfolio.copy(),
                }
            )

    def get_results(self):
        """
        Return the results of the backtest as a DataFrame.
        """
        return pd.DataFrame(self.results)

    def plot_results(self):
        """
        Plot the portfolio value over time.
        """
        results_df = self.get_results()
        results_df.set_index("date")["portfolio_value"].plot(
            title="Portfolio Value Over Time"
        )
