import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Live Token Dashboard", layout="wide")

st.title("📊 Live Token Price & RSI Dashboard")

# Token mapping with TradingView-compatible symbols
tokens = {
    "Realio Network": "BINANCE:RIOGBP",
    "PAAL AI": "BITGET:PAALGBP",
    "Nakamoto Games": "MEXC:NAKAGBP",
    "ANyONe Protocol": "MEXC:ANYONEGBP",
    "Devve": "MEXC:DEVVEGBP",
    "Propbase": "MEXC:PROPSGBP",
    "Propchain": "MEXC:PROPCGBP",
    "Energy Web Token": "KRAKEN:EWTGBP",
    "Bitcoin": "KRAKEN:XBTGBP",
    "Tether USDt": "KRAKEN:USDTGBP"
}

# Placeholder function to simulate TradingView price + RSI fetch
def fetch_tradingview_data(symbol):
    # In live production, connect via TradingView webhook or unofficial API
    # These are simulated static/dummy values for now
    dummy_prices = {
        "BINANCE:RIOGBP": 0.22,
        "BITGET:PAALGBP": 0.084,
        "MEXC:NAKAGBP": 0.31,
        "MEXC:ANYONEGBP": 0.43,
        "MEXC:DEVVEGBP": 0.40,
        "MEXC:PROPSGBP": 0.023,
        "MEXC:PROPCGBP": 0.47,
        "KRAKEN:EWTGBP": 1.15,
        "KRAKEN:XBTGBP": 77147,
        "KRAKEN:USDTGBP": 0.737
    }
    dummy_rsi = {
        "BINANCE:RIOGBP": (42.1, 45.7),
        "BITGET:PAALGBP": (38.9, 40.5),
        "MEXC:NAKAGBP": (52.3, 50.0),
        "MEXC:ANYONEGBP": (41.2, 46.9),
        "MEXC:DEVVEGBP": (57.8, 55.4),
        "MEXC:PROPSGBP": (35.6, 40.1),
        "MEXC:PROPCGBP": (47.2, 49.6),
        "KRAKEN:EWTGBP": (43.0, 45.0),
        "KRAKEN:XBTGBP": (58.0, 62.1),
        "KRAKEN:USDTGBP": (50.0, 50.0)
    }
    return dummy_prices.get(symbol, 0.0), dummy_rsi.get(symbol, ("—", "—"))

# Build display data
data = []
for name, symbol in tokens.items():
    price, (rsi_1h, rsi_4h) = fetch_tradingview_data(symbol)
    formatted_price = f"£{price:,.4f}" if price < 1000 else f"£{price:,.0f}"
    data.append({
        "Token": name,
        "Price (GBP)": formatted_price,
        "RSI (1H)": rsi_1h,
        "RSI (4H)": rsi_4h
    })

# Display as styled DataFrame
st.dataframe(pd.DataFrame(data), use_container_width=True)
