import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data

if __name__ == "__main__":

    with st.sidebar:
        st.markdown("""
                <style>
                    div[data-testid="stImage"] {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        width: 100%;
                        margin-top: -50px;
                    }
                    img {
                        border-radius: 50%;
                        width: 60% !important;
                    }
                    hr{
                        margin:0;
                    }
                </style>
        """, unsafe_allow_html=True)
        st.image("assets/logo.webp", width=200)
        st.empty()
        st.title("TradingBot")
        st.divider()
        st.selectbox("Select Asset", ["MLTrader"])
        with st.form("Trading Bot Experiment"):
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            submitted = st.form_submit_button("Run Backtest")
            if submitted:
                pass

    with st.container():
        with st.expander("Candlestick Chart"):
            renderLightweightCharts( [
                {
                    "chart": {},
                    "series": [{
                        "type": 'Candlestick',
                        "data": data.priceCandlestickMultipane,
                        "options": {}
                    }],
                }
            ], 'candlestick')
