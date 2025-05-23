import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Crypto Hedge Fund Dashboard", layout="wide")
st.title("🧠 Crypto Hedge Fund Strategy Dashboard")

# --- Portfolio Setup ---
st.subheader("📊 Current Holdings")
portfolio_data = {
    "Token": ["PAAL", "RIO", "PROPS", "NAKA", "ANYONE", "DEVVE", "PROPC", "USDT", "BTC"],
    "Units": [11400, 5003.06, 40840.88, 3182.46, 2200.78, 2003.85, 740, 1277.90, 0.0006414],
    "CoinGecko ID": ["paal-ai", "realio-network", "propbase", "nakamoto-games", "anyone", "devve", "propchain", "tether", "bitcoin"]
}
df = pd.DataFrame(portfolio_data)

# --- Batch Fetch Prices ---
all_ids = ",".join(df["CoinGecko ID"].tolist())
url = f"https://api.coingecko.com/api/v3/simple/price?ids={all_ids}&vs_currencies=gbp"
response = requests.get(url)
prices = response.json() if response.status_code == 200 else {}
df["Price (GBP)"] = df["CoinGecko ID"].apply(lambda x: prices.get(x, {}).get("gbp", 0))

# --- Manual Override for Missing Prices ---
for i in df.index:
    if df.loc[i, "Price (GBP)"] == 0:
        manual = st.number_input(f"Manual price for {df.loc[i, 'Token']} (GBP):", min_value=0.0, step=0.0001, key=df.loc[i, 'Token'])
        df.loc[i, "Price (GBP)"] = manual

df["Value (GBP)"] = df["Units"] * df["Price (GBP)"]
total_value = df["Value (GBP)"].sum()

st.dataframe(df[["Token", "Units", "Price (GBP)", "Value (GBP)"]], use_container_width=True)
st.metric("💷 Total Portfolio Value", f"£{total_value:,.2f}")

# --- KPI Summary ---
st.header("📈 Strategy KPI Summary")
usdt_available = df[df["Token"] == "USDT"]["Value (GBP)"].values[0]
st.metric("Vault Progress", "0.0641 BTC / 1 BTC", "6.41%")
st.metric("USDT Available", f"£{usdt_available:,.2f}")
st.metric("Harvest Realised (May)", "£257.60")

# --- BTC Vault Tracker ---
st.subheader("🏦 BTC Vault Tracker")
btc_target = 1.0
btc_current = df[df["Token"] == "BTC"]["Units"].values[0]
btc_progress = (btc_current / btc_target) * 100
st.progress(btc_progress / 100, text=f"{btc_progress:.2f}% of 1 BTC Goal")

# --- Risk Grading System ---
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
if usdt_available > 1000:
    st.success(f"You have £{usdt_available:.2f} in USDT. You may siphon £50 into BTC as a vault asset.")
else:
    st.info("USDT balance is below £1,000. No siphon suggested.")

# --- Staff Analyst Panels ---
st.header("🧠 Analyst Role Panels")
with st.expander("📡 Signal Analyst"):
    st.write("- BTC Dominance Chart")
    st.write("- ETH/BTC Ratio Tracker")
    st.write("- Altseason Signal Gauge")

with st.expander("📊 Weekly Report Assistant"):
    st.write("- Weekly ROI (bar chart: GBP vs BTC)")
    st.write("- Download latest PDF report")

with st.expander("🔄 Rotation Optimizer"):
    st.write("- Current over/underweighted tokens")
    st.write("- Suggested rebalances with %")

with st.expander("🧾 Harvest Trigger Assistant"):
    st.write("- Realized gain table")
    st.write("- Warning if harvest zone hit")

with st.expander("🌐 Market Sentiment Tracker"):
    st.write("- Social Sentiment Heatmap")
    st.write("- Narrative Rotation Score")

with st.expander("📋 Performance Auditor"):
    st.write("- TWR & MWR Calculations")
    st.write("- BTC-equivalent Chart vs Benchmark")

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
