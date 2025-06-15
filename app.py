import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Crypto Hedge Fund Dashboard", layout="wide")
st_autorefresh(interval=60000, key="refresh")
st.title("🧠 Crypto Hedge Fund Strategy Dashboard")

# --- Portfolio Setup ---
st.subheader("📊 Current Holdings")
portfolio_data = {
    "Token": ["PAAL", "RIO", "PROPS", "NAKA", "ANYONE", "DEVVE", "PROPC", "USDT", "BTC"],
    "Units": [11400, 5003.06, 40840.88, 3182.46, 2200.78, 2003.85, 740, 1277.90, 0.0006414],
    "CoinGecko ID": ["paal-ai", "realio-network", "propbase", "nakamoto-games", "anyone-protocol", "devve", "propchain", "tether", "bitcoin"]
}
df = pd.DataFrame(portfolio_data)

# --- Fetch Prices ---
all_ids = ",".join(df["CoinGecko ID"].tolist())
url = f"https://api.coingecko.com/api/v3/simple/price?ids={all_ids}&vs_currencies=gbp"
response = requests.get(url)
prices = response.json() if response.status_code == 200 else {}
df["Price (GBP)"] = df["CoinGecko ID"].apply(lambda x: prices.get(x, {}).get("gbp", 0))

# --- Manual Price Overrides ---
for i in df.index:
    if df.loc[i, "Price (GBP)"] == 0:
        manual = st.number_input(f"Manual price for {df.loc[i, 'Token']} (GBP):", min_value=0.0, step=0.0001, key=df.loc[i, 'Token'])
        df.loc[i, "Price (GBP)"] = manual

df["Value (GBP)"] = df["Units"] * df["Price (GBP)"]
total_value = df["Value (GBP)"].sum()

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
