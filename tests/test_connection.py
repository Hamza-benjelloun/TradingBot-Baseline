from src.broker import get_broker

def test_get_broker():
    broker = get_broker()
    assert broker is not None