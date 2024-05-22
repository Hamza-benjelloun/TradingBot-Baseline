from src.broker import get_streamer

async def stream_handler(quote):
    print(quote)
    print(type(quote))


def test_get_streamer():
    streamer = get_streamer()
    streamer.subscribe_quotes(stream_handler, "SPY")
    streamer.run()
    assert streamer is not None