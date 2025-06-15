import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Live Token Dashboard", layout="wide")

st.title("📊 Live Token Price & RSI Dashboard")

# Token mapping with fallback manual prices for unsupported tokens
tokens = {
    "Realio Network": "RIOUSDT",
    "PAAL AI": "PAALUSDT",
    "Nakamoto Games": "NAKAUSDT",
    "ANyONe Protocol": "ANYONEUSDT",
    "Devve": "DEVVEUSDT",
    "Propbase": "PROPSUSDT",
    "Propchain": "PROPCUSDT",
    "Energy Web Token": "EWTUSDT",
    "Bitcoin": "BTCUSDT",
    "Tether USDt": "USDTUSDT"
}

# Function to fetch prices from TradingView (mocked via random API or static for now)
def fetch_price(symbol):
    try:
        # Here you would connect to a real TV or exchange feed
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url).json()
        price = float(res['price'])
        return price
    except:
        return 0.0

# Manual GBP conversion rates for non-GBP feeds
usd_to_gbp = 0.79

# Create data table
data = []
for name, symbol in tokens.items():
    price_usd = fetch_price(symbol)
    price_gbp = price_usd * usd_to_gbp
    formatted_price = f"£{price_gbp:,.4f}" if price_gbp < 1000 else f"£{price_gbp:,.0f}"
    data.append({"Token": name, "Price (GBP)": formatted_price, "RSI (1H)": "—", "RSI (4H)": "—"})

# Display
st.dataframe(pd.DataFrame(data))
