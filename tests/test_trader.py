import os

from src.trader import Trader


def test_is_market_open():
    os.environ["ENV"] = "preprod"
    assert Trader().is_market_open() == False
    os.environ["ENV"] = "dev"
    assert Trader().is_market_open() == True


def test_account_cash():
    os.environ["ENV"] = "preprod"
    assert Trader().initial_capital == 1000000
    os.environ["ENV"] = "dev"
    assert Trader().initial_capital == 100000


def test_has_sufficient_buying_power():
    assert Trader().has_sufficient_buying_power(100, 100) == True


def test_within_risk_tolerance():
    assert Trader().within_risk_tolerance(100, 10) == True


def test_can_add_position():
    assert Trader().can_add_position() == True


def test_calculate_position_size():
    os.environ["ENV"] = "preprod"
    assert Trader().calculate_position_size(100, 90) == 2000
    assert Trader().calculate_position_size(100, 100) == 0
    os.environ["ENV"] = "dev"
    assert Trader().calculate_position_size(100, 90) == 200
    assert Trader().calculate_position_size(100, 100) == 0
