
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="AutoMargin Mobile App", layout="wide")
st.title("AutoMargin: VIN Profit Analyzer")
st.markdown("Upload a VIN list or enter a single VIN to compare auction pricing and flag profitable flips.")

# Fee Configuration
fees = {
    "Buy Fee": 300,
    "Sell Fee": 300,
    "DealShield": 245,
    "Transport": 125,
    "Software Fee": 10,
    "Target Profit": 400
}

def simulate_mmr():
    return random.randint(4000, 7000)

def simulate_edge_price(mmr):
    return mmr + random.randint(600, 1800)

def calculate_profit(mmr, edge_sale):
    total_cost = mmr + sum(fees.values()) - fees["Target Profit"]
    profit = edge_sale - total_cost
    meets_target = profit >= fees["Target Profit"]
    return total_cost, profit, meets_target

# --- Sidebar Input ---
st.sidebar.header("Single VIN Lookup")
single_vin = st.sidebar.text_input("Enter VIN")

# --- Single VIN Result ---
if single_vin:
    st.subheader("Single VIN Analysis")
    mmr = simulate_mmr()
    edge = simulate_edge_price(mmr)
    cost, profit, meets = calculate_profit(mmr, edge)
    vin_df = pd.DataFrame([{
        "VIN": single_vin,
        "MMR": mmr,
        "Edge Sale Price": edge,
        "Total Cost": cost,
        "Profit": profit,
        "Meets Target": meets
    }])
    st.dataframe(vin_df)

# --- CSV Upload ---
st.subheader("Run List Upload")
uploaded_file = st.file_uploader("Upload a CSV with a VIN column", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "VIN" not in df.columns:
            st.error("CSV must have a 'VIN' column.")
        else:
            df["MMR"] = df["VIN"].apply(lambda x: simulate_mmr())
            df["Edge Sale Price"] = df["MMR"].apply(simulate_edge_price)
            df["Total Cost"] = df["MMR"] + sum(fees.values()) - fees["Target Profit"]
            df["Profit"] = df["Edge Sale Price"] - df["Total Cost"]
            df["Meets Target"] = df["Profit"] >= fees["Target Profit"]

            st.success("Analysis complete. Scroll to view results.")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="AutoMargin_Results.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Failed to process file: {e}")
else:
    st.info("Please upload a CSV file with VINs or enter a single VIN to begin analysis.")
