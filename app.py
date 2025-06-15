import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Token Dashboard", layout="wide")
st_autorefresh(interval=60000, key="refresh")  # Auto-refresh every 60 seconds

st.title("📊 Live Token Price & RSI Dashboard")

# Token mapping with live-friendly symbols (CoinGecko + Binance + Kraken)
tokens = {
    "Realio Network": "realio-network",
    "PAAL AI": "paal-ai",
    "Nakamoto Games": "nakamoto-games",
    "ANyONe Protocol": "anyone",
    "Devve": "devve",
    "Propbase": "props",
    "Propchain": "propchain",
    "Energy Web Token": "energy-web-token",
    "Bitcoin": "bitcoin",
    "Tether USDt": "tether"
}

# Function to fetch GBP prices from CoinGecko
def fetch_prices(token_dict):
    ids = ",".join(token_dict.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=gbp"
    res = requests.get(url).json()
    return {name: res.get(cid, {}).get("gbp", 0.0) for name, cid in token_dict.items()}

# Function placeholder for RSI values (replace with TradingView fetch later)
def fetch_rsi(symbol):
    return ("Loading", "Loading")  # To be replaced with webhook or API connection

# Fetch live data
price_data = fetch_prices(tokens)

# Build display table
data = []
for name in tokens:
    price = price_data.get(name, 0.0)
    price_fmt = f"£{price:,.4f}" if price < 1000 else f"£{price:,.0f}"
    rsi_1h, rsi_4h = fetch_rsi(name)
    data.append({"Token": name, "Price (GBP)": price_fmt, "RSI (1H)": rsi_1h, "RSI (4H)": rsi_4h})

# Display
st.dataframe(pd.DataFrame(data), use_container_width=True)
