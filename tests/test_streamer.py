import os
from time import sleep

from loguru import logger

from src.client import get_streamer
from src.trader import Trader


async def stream_handler(quote):
    logger.info(quote)


def test_get_streamer():
    streamer = get_streamer()
    os.environ["ENV"] = "preprod"
    if Trader().is_market_open():
        streamer.subscribe_quotes(stream_handler, "SPY")
        streamer.run()
        sleep(3)
        streamer.stop()
    assert streamer is not None
