import requests
import pandas as pd
import streamlit as st

st.title("📊 Live Token Price & RSI Dashboard")

# Token mapping
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

# Fetch prices from CoinGecko
ids = ",".join(tokens.values())
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=gbp"
prices = requests.get(url).json()

# Display table
data = [{"Token": name, "Price (£)": prices[gecko_id]["gbp"]} for name, gecko_id in tokens.items()]
df = pd.DataFrame(data)
st.dataframe(df)

