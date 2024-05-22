from lumibot.strategies.strategy import Strategy
from src.broker import BASE_URL,API_KEY,API_SECRET



import pandas as pd
import numpy as np

class Trader:
    def __init__(self, initial_capital=100000.0, risk_tolerance=0.02, max_positions=10):
        """
        Initialize the Trader with an initial capital, risk tolerance, and maximum number of positions.

        :param initial_capital: The starting capital for trading.
        :param risk_tolerance: The percentage of capital to risk per trade.
        :param max_positions: The maximum number of different assets to hold.
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.portfolio = {}
        self.trades = []
        self.risk_tolerance = risk_tolerance
        self.max_positions = max_positions

    def is_market_open(self):
        """
        Check if the market is open. This is a placeholder and should be implemented with actual market hours.

        :return: Boolean indicating if the market is open.
        """
        # Placeholder for actual market hours check
        return True

    def has_sufficient_buying_power(self, price, quantity):
        """
        Check if there is enough cash to execute the buy order.

        :param price: The price at which to buy.
        :param quantity: The quantity to buy.
        :return: Boolean indicating if there is sufficient buying power.
        """
        return self.cash >= price * quantity

    def within_risk_tolerance(self, price, quantity):
        """
        Check if the trade is within the risk tolerance.

        :param price: The price at which to trade.
        :param quantity: The quantity to trade.
        :return: Boolean indicating if the trade is within the risk tolerance.
        """
        potential_loss = price * quantity
        return potential_loss <= self.initial_capital * self.risk_tolerance

    def can_add_position(self):
        """
        Check if a new position can be added without exceeding the maximum number of positions.

        :return: Boolean indicating if a new position can be added.
        """
        return len(self.portfolio) < self.max_positions

    def calculate_position_size(self, price, stop_loss):
        """
        Calculate the position size based on risk tolerance and stop-loss.

        :param price: The price at which to buy.
        :param stop_loss: The stop-loss price.
        :return: The quantity to buy.
        """
        risk_per_share = price - stop_loss
        if risk_per_share <= 0:
            return 0
        risk_per_trade = self.initial_capital * self.risk_tolerance
        quantity = risk_per_trade // risk_per_share
        return int(quantity)

    def buy(self, ticker, price, stop_loss):
        """
        Execute a buy order with risk management.

        :param ticker: The ticker symbol of the asset.
        :param price: The price at which to buy.
        :param stop_loss: The stop-loss price.
        """
        quantity = self.calculate_position_size(price, stop_loss)
        if quantity > 0 and self.is_market_open() and self.has_sufficient_buying_power(price, quantity) and self.within_risk_tolerance(price, quantity) and self.can_add_position():
            total_cost = price * quantity
            self.cash -= total_cost
            if ticker in self.portfolio:
                self.portfolio[ticker]['quantity'] += quantity
            else:
                self.portfolio[ticker] = {'quantity': quantity, 'stop_loss': stop_loss}
            self.trades.append({'action': 'buy', 'ticker': ticker, 'price': price, 'quantity': quantity, 'stop_loss': stop_loss})
        else:
            print("Cannot execute buy order. Check market status, buying power, risk tolerance, and position limits.")

    def sell(self, ticker, price, quantity):
        """
        Execute a sell order.

        :param ticker: The ticker symbol of the asset.
        :param price: The price at which to sell.
        :param quantity: The quantity to sell.
        """
        if ticker in self.portfolio and self.portfolio[ticker]['quantity'] >= quantity:
            total_gain = price * quantity
            self.cash += total_gain
            self.portfolio[ticker]['quantity'] -= quantity
            self.trades.append({'action': 'sell', 'ticker': ticker, 'price': price, 'quantity': quantity})
            if self.portfolio[ticker]['quantity'] == 0:
                del self.portfolio[ticker]
        else:
            print("Cannot execute sell order. Insufficient quantity to sell.")

    def calculate_portfolio_value(self, current_prices):
        """
        Calculate the total value of the portfolio based on current prices.

        :param current_prices: A dictionary of current prices for each asset.
        :return: The total value of the portfolio.
        """
        portfolio_value = self.cash
        for ticker, position in self.portfolio.items():
            if ticker in current_prices:
                portfolio_value += current_prices[ticker] * position['quantity']
        return portfolio_value

    def get_trades(self):
        """
        Get the list of executed trades.

        :return: A DataFrame containing the trades.
        """
        return pd.DataFrame(self.trades)

# Example of a specific trader inheriting from the Trader base class
class SimpleTrader(Trader):
    def __init__(self, initial_capital=100000.0, risk_tolerance=0.02, max_positions=10):
        super().__init__(initial_capital, risk_tolerance, max_positions)

    def execute_trade(self, signal, ticker, price, stop_loss):
        """
        Execute trades based on the provided signal.

        :param signal: The trading signal (1 for buy, -1 for sell, 0 for hold).
        :param ticker: The ticker symbol of the asset.
        :param price: The price at which to trade.
        :param stop_loss: The stop-loss price.
        """
        if signal == 1:
            self.buy(ticker, price, stop_loss)
        elif signal == -1:
            quantity = self.portfolio.get(ticker, {}).get('quantity', 0)
            self.sell(ticker, price, quantity)

# Usage
data = pd.DataFrame({
    'Close': [100, 102, 104, 103, 105, 107, 106, 108, 109, 107]
})

trader = SimpleTrader(initial_capital=100000)
current_prices = {'AAPL': 150}
trader.execute_trade(1, 'AAPL', current_prices['AAPL'], stop_loss=140)
print(trader.get_trades())
print("Portfolio Value:", trader.calculate_portfolio_value(current_prices))