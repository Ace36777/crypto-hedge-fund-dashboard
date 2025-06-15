
import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh
from tradingview_ta import TA_Handler, Interval

st.set_page_config(page_title="Live Token Dashboard", layout="wide")
st_autorefresh(interval=60000, key="refresh")  # Auto-refresh every 60 seconds

st.title("📊 Live Token Price & RSI Dashboard")

# Token mapping with CoinGecko slugs, TradingView symbols, and exchange info
tokens = {
    "Realio Network": {"cg": "realio-network", "tv": "RIOUSDT", "exchange": "KUCOIN"},
    "PAAL AI": {"cg": "paal-ai", "tv": "PAALUSDT", "exchange": "KUCOIN"},
    "Nakamoto Games": {"cg": "nakamoto-games", "tv": "NAKAUSDT", "exchange": "KUCOIN"},
    "ANyONe Protocol": {"cg": "anyone", "tv": "ANYONEUSDT", "exchange": "GATEIO"},
    "Devve": {"cg": "devve", "tv": "DEVVEUSDT", "exchange": "BITMART"},
    "Propbase": {"cg": "props", "tv": "PROPSUSDT", "exchange": "BITMART"},
    "Propchain": {"cg": "propchain", "tv": "PROPCUSDT", "exchange": "KUCOIN"},
    "Energy Web Token": {"cg": "energy-web-token", "tv": "EWTUSDT", "exchange": "KUCOIN"},
    "Bitcoin": {"cg": "bitcoin", "tv": "BTCUSDT", "exchange": "BINANCE"},
    "Tether USDt": {"cg": "tether", "tv": "USDTUSDT", "exchange": "BINANCE"}
}

# Fetch GBP prices from CoinGecko
def fetch_prices(token_dict):
    ids = ",".join([info["cg"] for info in token_dict.values()])
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=gbp"
    try:
        res = requests.get(url).json()
        return {name: res.get(info["cg"], {}).get("gbp", 0.0) for name, info in token_dict.items()}
    except Exception as e:
        print(f"[ERROR] Price fetch failed: {e}")
        return {name: 0.0 for name in token_dict}

# Fetch RSI using tradingview_ta
def fetch_rsi(symbol, exchange):
    try:
        handler_1h = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="crypto",
            interval=Interval.INTERVAL_1_HOUR
        )
        handler_4h = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="crypto",
            interval=Interval.INTERVAL_4_HOURS
        )
        rsi_1h = handler_1h.get_analysis().indicators.get("RSI", "N/A")
        rsi_4h = handler_4h.get_analysis().indicators.get("RSI", "N/A")
        return (round(rsi_1h, 2), round(rsi_4h, 2))
    except Exception as e:
        print(f"[ERROR] RSI fetch failed for {symbol} on {exchange}: {e}")
        return ("Error", "Error")

# Fetch live data
price_data = fetch_prices(tokens)

# Build display table
data = []
for name, info in tokens.items():
    price = price_data.get(name, 0.0)
    price_fmt = f"£{price:,.4f}" if price < 1000 else f"£{price:,.0f}"
    rsi_1h, rsi_4h = fetch_rsi(info["tv"], info["exchange"])
    data.append({"Token": name, "Price (GBP)": price_fmt, "RSI (1H)": rsi_1h, "RSI (4H)": rsi_4h})

# Display
st.dataframe(pd.DataFrame(data), use_container_width=True)
