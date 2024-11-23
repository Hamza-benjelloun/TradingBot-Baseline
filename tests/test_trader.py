from src.trader import Trader
import pytest


@pytest.fixture
def trader():
    return Trader()


def test_is_market_open(trader):
    assert trader.is_market_open() == False

def test_account_cash(trader):
    assert trader.initial_capital == 1000000

def test_has_sufficient_buying_power(trader):
    assert trader.has_sufficient_buying_power(100, 100) == True

def test_within_risk_tolerance(trader):
    assert trader.within_risk_tolerance(100, 10) == True

def test_can_add_position(trader):
    assert trader.can_add_position() == True

def test_calculate_position_size(trader):
    assert trader.calculate_position_size(100, 90) == 2000
    assert trader.calculate_position_size(100, 100) == 0