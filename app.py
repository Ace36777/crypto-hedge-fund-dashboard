import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="Crypto Hedge Fund Dashboard", layout="wide")
st_autorefresh(interval=60000, key="refresh")
st.title("🧠 Crypto Hedge Fund Strategy Dashboard")

# --- File Uploads ---
st.sidebar.header("📂 Upload Analyst Reports")
pdf = st.sidebar.file_uploader("Upload PDF Report", type=["pdf"])
if pdf:
    st.sidebar.success(f"Uploaded: {pdf.name}")

# --- Simulated Capital Injection Log (CSV Placeholder) ---
log_file = "capital_injection_log.csv"
if not os.path.exists(log_file):
    pd.DataFrame({"Date": [], "Amount (GBP)": []}).to_csv(log_file, index=False)

st.sidebar.subheader("📥 Capital Injections")
with st.sidebar.form("Add Injection"):
    date = st.date_input("Injection Date")
    amount = st.number_input("Amount (GBP)", min_value=0.0)
    submitted = st.form_submit_button("Log Injection")
    if submitted:
        df_log = pd.read_csv(log_file)
        df_log = pd.concat([df_log, pd.DataFrame([{"Date": date, "Amount (GBP)": amount}])], ignore_index=True)
        df_log.to_csv(log_file, index=False)
        st.success("Injection logged successfully")

injection_data = pd.read_csv(log_file)

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

# --- Sniper Zone Tracker ---
sniper_thresholds = {"PAAL": 0.11, "RIO": 0.22, "PROPS": 0.023, "NAKA": 0.29, "DEVVE": 0.38, "PROPC": 0.42}
sniper_df = df[df["Token"].isin(sniper_thresholds.keys())].copy()
sniper_df["In Buy Zone"] = sniper_df.apply(lambda x: "🟢" if x["Price (GBP)"] <= sniper_thresholds[x["Token"]] else "🔴", axis=1)

st.dataframe(df[["Token", "Units", "Price (GBP)", "Value (GBP)"]], use_container_width=True)
st.metric("💷 Total Portfolio Value", f"£{total_value:,.2f}")

st.subheader("🎯 Sniper Buy Zone Tracker")
st.dataframe(sniper_df[["Token", "Price (GBP)", "In Buy Zone"]], use_container_width=True)

# --- KPI Summary ---
st.header("📈 Strategy KPI Summary")
usdt_available = df[df["Token"] == "USDT"]["Value (GBP)"].values[0]
st.metric("Vault Progress", "0.0641 BTC / 1 BTC", "6.41%")
st.metric("USDT Available", f"£{usdt_available:,.2f}")
st.metric("Harvest Realised (May)", "£257.60")

# --- Injection Timeline ---
st.subheader("📆 Capital Injection History")
st.dataframe(injection_data.tail(10))

# --- Staff Role Panel Preview: Accumulation Strategy & Simulation ---
st.header("📊 Accumulation Strategy & Simulation")
st.markdown("This section mirrors compounder simulations from analyst reports")
compounders = ["RIO", "PAAL", "PROPS", "NAKA", "DEVVE", "ANYONE", "PROPC"]

# Editable Target Units
st.sidebar.subheader("🎯 Set Target Units")
target_units_input = {}
for token in compounders:
    default_target = {
        "RIO": 10000, "PAAL": 20000, "PROPS": 80000,
        "NAKA": 6000, "DEVVE": 5000, "ANYONE": 5000, "PROPC": 2000
    }.get(token, 0)
    target_units_input[token] = st.sidebar.number_input(f"Target Units for {token}", value=default_target, min_value=0, step=1)

for token in compounders:
    current_row = df[df["Token"] == token]
    if not current_row.empty:
        st.subheader(f"📌 {token}: Simulation")
        current_price = current_row["Price (GBP)"].values[0]
        units = current_row["Units"].values[0]
        target_units = target_units_input[token]
        remaining = target_units - units
        harvest_prices = [current_price * (1 + pct/100) for pct in [25, 50, 75]]
        value_at_targets = [harvest * target_units for harvest in harvest_prices]

        sim_df = pd.DataFrame({
            "Live Price": [current_price] * 3,
            "Scenario": ["+25%", "+50%", "+75%"],
            "Harvest Price": harvest_prices,
            "Value @ Target Units": value_at_targets
        })
        st.dataframe(sim_df)

# --- Footer ---
st.caption("Fully upgraded dashboard with simulation, sniper tracking, staff KPIs and reporting tools")
