import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Page config
st.set_page_config(page_title="Crypto Hedge Fund Dashboard", layout="wide")
st.title("🧠 Crypto Hedge Fund Strategy Dashboard")

# --- Live Price Fetcher ---
def fetch_price(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=gbp"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get(token_id, {}).get("gbp", 0.0)
    return 0.0

# --- Portfolio Setup ---
st.subheader("📊 Current Holdings")
portfolio_data = {
    "Token": ["PAAL", "RIO", "PROPS", "NAKA", "ANYONE", "DEVVE", "PROPC", "USDT", "BTC"],
    "Units": [11400, 5003.06, 40840.88, 3182.46, 2200.78, 2003.85, 740, 1277.90, 0.0006414],
    "CoinGecko ID": ["paal-ai", "realio-network", "props-token", "nakamoto-games", "anyone-ai", "devve", "propcraft", "tether", "bitcoin"]
}
df = pd.DataFrame(portfolio_data)

# Fetch live prices and calculate value
df["Price (GBP)"] = df["CoinGecko ID"].apply(fetch_price)
df["Value (GBP)"] = df["Units"] * df["Price (GBP)"]
total_value = df["Value (GBP)"].sum()

st.dataframe(df[["Token", "Units", "Price (GBP)", "Value (GBP)"]], use_container_width=True)
st.metric("💷 Total Portfolio Value", f"£{total_value:,.2f}")

# --- BTC Vault Tracker ---
st.subheader("🏦 BTC Vault Tracker")
btc_target = 1.0
btc_current = df[df["Token"] == "BTC"]["Units"].values[0]
btc_progress = (btc_current / btc_target) * 100
st.progress(btc_progress / 100, text=f"{btc_progress:.2f}% of 1 BTC Goal")

# --- Risk Grading System (manual entry placeholder) ---
st.subheader("📉 Weekly Risk Grades")
risk_data = {
    "Token": df["Token"].tolist(),
    "Volatility": [3, 2, 2, 3, 3, 4, 2, 1, 1],
    "Narrative": [5, 4, 3, 3, 5, 3, 3, 1, 3],
    "Liquidity": [3, 2, 2, 3, 3, 2, 2, 5, 5],
    "Harvest Readiness": [2, 3, 2, 3, 2, 2, 4, 1, 1]
}
risk_df = pd.DataFrame(risk_data)
risk_df["Avg Score"] = risk_df[["Volatility", "Narrative", "Liquidity", "Harvest Readiness"]].mean(axis=1)
risk_df["Risk Level"] = pd.cut(risk_df["Avg Score"], bins=[0,2.5,2.9,3.4,5], labels=["Low", "Med-Low", "Medium", "High"])
st.dataframe(risk_df, use_container_width=True)

# --- Compounder Simulation ---
st.subheader("📈 Compounder Simulation")
selected_token = st.selectbox("Choose a token to simulate harvest", df["Token"].unique())
token_row = df[df["Token"] == selected_token]
if not token_row.empty:
    current_price = token_row["Price (GBP)"].values[0]
    units_held = token_row["Units"].values[0]
    harvest_prices = [current_price * m for m in [1.25, 1.5, 1.75]]
    simulation = pd.DataFrame({
        "Harvest Price (GBP)": harvest_prices,
        "Value at Harvest": [p * units_held for p in harvest_prices],
        "% Gain": [(p - current_price)/current_price * 100 for p in harvest_prices]
    })
    st.dataframe(simulation, use_container_width=True)

# --- Vault Siphon Logic ---
st.subheader("🔁 Vault Siphon Proposal")
vault_suggested = False
usdt_value = df[df["Token"] == "USDT"]["Value (GBP)"].values[0]
if usdt_value > 1000:
    st.success(f"You have £{usdt_value:.2f} in USDT. You may siphon £50 into BTC as a vault asset.")
    vault_suggested = True
else:
    st.info("USDT balance is below £1,000. No siphon suggested.")

# --- Tactical Calendar ---
st.subheader("📅 Weekly Tactical Calendar")
calendar = {
    "Monday": "🔍 Review market news and BTC.D",
    "Tuesday": "💰 Deploy sniper bids (e.g., PROPC, RIO)",
    "Wednesday": "📊 Check midweek RSI signals",
    "Thursday": "📈 Prepare weekend accumulation plays",
    "Friday": "🧠 Re-evaluate narratives and social buzz",
    "Saturday": "⏳ Monitor BTC volatility & USDT triggers",
    "Sunday": "🧾 Run weekly reports + rebalance alerts"
}
st.table(pd.DataFrame(list(calendar.items()), columns=["Day", "Action Plan"]))

# --- Footer ---
st.caption("Automated dashboard powered by Streamlit + CoinGecko API + your BTC pricing data")
