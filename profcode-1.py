#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
finance_dashboard_pipeline.py

This script synthesizes the key lessons from the Python for Finance lectures:
- Download financial and macroeconomic data (yfinance + FRED)
- Save and reload data from CSV files
- Handle missing values correctly (forward fill, no interpolation)
- Compute arithmetic returns
- Compute cumulative compounded returns (growth indexes)
- Plot and save charts
- Write modular code (each function does one thing only)

Author: Alexandre Landi (Skema Business School)
Academic Year 2025/26 — Fall 2025
"""

# -----------------------------
# Imports
# -----------------------------
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pandas_datareader import data as dr
import streamlit as st 

# to run streamlit : streamlit run streamlit_app.py
# to stop press control c 
# documentation for streamlit.  https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect


# ============================================
# Import Block
# ============================================

#import pandas as pd
#port yfinance as yf
#mport matplotlib.pyplot as plt
##import pandas_datareader.data as dr
#import streamlit as st

# pandas: provides powerful tools for handling time series and tabular data.
# yfinance: downloads asset price data directly from Yahoo Finance.
# matplotlib: generates plots and visualizations.
# pandas datareader: fetches macroeconomic indicators from FRED.
# streamlit: creates an interactive dashboard.


# ============================================
# Function Definitions
# ============================================

def download_yfinance_close(ticker, start, end):
    raw_data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False
    )
    price_data = raw_data[["Close"]].rename(columns={"Close": ticker})
    return price_data
# Downloads adjusted close prices from Yahoo Finance (only "Close" column, renamed with ticker).

def download_fred(series, start):
    fred_data = dr.DataReader(series, data_source="fred", start=start)
    return fred_data
# Queries the FRED database for one or multiple macroeconomic series (e.g., CPI, GDP).

def save_csv(dataframe, filename):
    dataframe.to_csv(filename)

def load_csv(filename):
    dataframe = pd.read_csv(filename, index_col=0, parse_dates=True)
    return dataframe
# Saving/loading CSV ensures reproducibility and avoids reliance on APIs every time.

def preprocess_data(dataframe):
    dataframe = dataframe.ffill()
    dataframe = dataframe.dropna()
    return dataframe
# Forward-fills missing values, then drops remaining leading NaN values.

def pct_change(dataframe):
    arithmetic_returns = dataframe.pct_change()
    return arithmetic_returns
# Computes arithmetic returns.

def compound_from_arithmetic(arithmetic_returns):
    cumulative_returns = (1 + arithmetic_returns).cumprod()
    return cumulative_returns
# Compounds arithmetic returns to cumulative growth indices.

def plot_series(dataframe, title, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 5))
    dataframe.plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Date")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
# Plots a DataFrame and saves the figure. Closing avoids overlap between multiple plots.


# ============================================
# Download Data Block
# ============================================

start_date = "2000-01-01"
end_date = "2025-09-09"

fred_series = ["CPIAUCNS", "GDP"]
macroeconomic_data = download_fred(fred_series, start=start_date)

tickers_and_files = {
    "ES=F": "SnP.csv",
    "ZN=F": "Treasuries.csv",
    "GC=F": "Gold.csv",
    "CL=F": "Crude.csv",
    "ZW=F": "Wheat.csv",
    "DX=F": "USD.csv"
}

assets_data = {}
for ticker, filename in tickers_and_files.items():
    assets_data[ticker] = download_yfinance_close(ticker, start_date, end_date)
# Downloaded equities, bonds, commodities, and dollar index for cross-asset perspective.


# ============================================
# Data Alignment
# ============================================

all_start_dates = [macroeconomic_data.index.min()]
for df in assets_data.values():
    all_start_dates.append(df.index.min())
common_start = max(all_start_dates)

macroeconomic_data = macroeconomic_data.loc[macroeconomic_data.index >= common_start]
for ticker in assets_data:
    assets_data[ticker] = assets_data[ticker].loc[assets_data[ticker].index >= common_start]
# Ensures all series cover the same time span, avoiding misleading comparisons.


# ============================================
# Write and Read CSV Blocks
# ============================================

save_csv(macroeconomic_data, "macro.csv")
for ticker, df in assets_data.items():
    save_csv(df, tickers_and_files[ticker])

# Alternative (reuse saved data instead of APIs):
# macroeconomic_data = load_csv("macro.csv")
# assets_data = {ticker: load_csv(file) for ticker, file in tickers_and_files.items()}


# ============================================
# Main Workflow
# ============================================

macroeconomic_data = preprocess_data(macroeconomic_data)
macroeconomic_returns = pct_change(macroeconomic_data)
macro_cumulative_returns = compound_from_arithmetic(macroeconomic_returns)

plot_series(macro_cumulative_returns,
            "Cumulative Growth of CPI and GDP",
            "Index",
            "macro_only.png")

all_assets_cumulative = pd.DataFrame()
for ticker, df in assets_data.items():
    df = preprocess_data(df)
    asset_returns = pct_change(df)
    asset_cumulative = compound_from_arithmetic(asset_returns)
    all_assets_cumulative[ticker] = asset_cumulative[ticker]

plot_series(all_assets_cumulative,
            "Cumulative Growth of Financial Assets",
            "Cumulative Growth",
            "assets_only.png")
# Produces two plots: one for macroeconomic series, one for financial assets.


# ============================================
# Final Report
# ============================================

print("\n=== Pipeline Finished Successfully ===\n")
macro_start = macroeconomic_data.index.min().strftime("%Y-%m-%d")
macro_end = macroeconomic_data.index.max().strftime("%Y-%m-%d")
print(f"Macroeconomic data: {macro_start} to {macro_end}, saved to macro.csv")

print("Financial assets:")
for ticker, filename in tickers_and_files.items():
    df = assets_data[ticker]
    start = df.index.min().strftime("%Y-%m-%d")
    end = df.index.max().strftime("%Y-%m-%d")
    print(f" - {ticker}: {start} to {end}, saved to {filename}")
# Confirms which data was used, saved, and the time range.

# ============================================
# Streamlit Dashboard
# ============================================

st.set_page_config("Cross-Asset Regime Monitor", layout="wide")
st.title("Cross-Asset Regime Monitor")

combined_cumulative = pd.concat(
    [macro_cumulative_returns, all_assets_cumulative], axis=1
).dropna()

available_assets = combined_cumulative.columns.tolist()
min_date = combined_cumulative.index.min()
max_date = combined_cumulative.index.max()

with st.sidebar:
    st.header("Dashboard Controls")
    selected_assets = st.multiselect("Select assets:", options=available_assets,
                                     default=available_assets)
    date_range = st.date_input("Date range:",
                               value=(min_date, max_date),
                               min_value=min_date,
                               max_value=max_date)

if selected_assets:
    filtered_data = combined_cumulative[selected_assets]
else:
    filtered_data = combined_cumulative.copy()

start, end = date_range
filtered_data = filtered_data.loc[start:end]

st.subheader("Cumulative Returns Table")
st.dataframe(filtered_data)

fig_all, ax_all = plt.subplots(figsize=(10, 5))
combined_cumulative.plot(ax=ax_all)
ax_all.set_title("Cumulative Growth of All Series")
st.pyplot(fig_all)

fig_selected, ax_selected = plt.subplots(figsize=(10, 5))
filtered_data.plot(ax=ax_selected)
ax_selected.set_title("Cumulative Growth of Selected Series")
st.pyplot(fig_selected)
# Streamlit app: lets user select assets and date ranges, shows table and plots (all vs selected).