from lumibot.brokers import Alpaca
from alpaca.data.live.stock import StockDataStream
from alpaca.data import StockHistoricalDataClient
import streamlit as st

API_KEY = st.secrets.get('API_KEY')
API_SECRET = st.secrets.get('API_SECRET')
BASE_URL = st.secrets.get('BASE_URL')
IS_PAPER = st.secrets.get('PAPER', True)

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": IS_PAPER,
}

@st.cache_resource
def get_broker():
    return Alpaca(ALPACA_CREDS)

@st.cache_resource
def get_streamer():
    return StockDataStream(
        api_key=API_KEY,
        secret_key=API_SECRET,
    )

@st.cache_resource
def get_historical_data():
    return StockHistoricalDataClient(
        api_key=API_KEY,
        secret_key=API_SECRET,
    )