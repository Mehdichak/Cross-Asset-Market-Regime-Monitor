

# to run streamlit : streamlit run streamlit_app.py
# to stop press control c 
# documentation for streamlit.  https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect


# ============================================
# Import Block
# ============================================


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

from datetime import date
start_date = "2000-01-01"
end_date = date.today().strftime("%Y-%m-%d")  # today's date dynamically

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

## ============================================
# Streamlit Dashboard
# ============================================

# ============================================
# Streamlit Dashboard
# ============================================
import datetime as dt
import matplotlib as mpl
import pandas as pd
import plotly.graph_objects as go  # <-- interactif pour le hover

# ---- Page config ----
st.set_page_config("Cross-Asset Regime Monitor", layout="wide")

# ---- Rosé Pine Moon inspired colors ----
rose_pine_colors = [
    "#eb6f92",  # rose
    "#9ccfd8",  # teal
    "#f6c177",  # gold
    "#c4a7e7",  # lavender
    "#31748f",  # pine
    "#e0def4",  # snow
    "#524f67",  # muted grey
]

# (Conserve ces rcParams même si le tracé principal est en Plotly :
# ils gardent la cohérence pour d’éventuels tracés Matplotlib.)
mpl.rcParams.update({
    "axes.facecolor": "#191724",
    "figure.facecolor": "#191724",
    "axes.edgecolor": "#e0def4",
    "axes.labelcolor": "#e0def4",
    "xtick.color": "#e0def4",
    "ytick.color": "#e0def4",
    "grid.color": "#524f67",
    "text.color": "#e0def4",
    "legend.edgecolor": "#191724",
})

# ---- Dashboard title ----
st.title("Cross-Asset Regime Monitor")

# ---- Combine macro & assets ----
combined_cumulative = pd.concat(
    [macro_cumulative_returns, all_assets_cumulative], axis=1
).dropna(how="all")

if combined_cumulative.empty:
    st.error("No data available.")
    st.stop()

available_assets = combined_cumulative.columns.tolist()

# Forcer Timestamp "naive" (sans timezone)
data_min = pd.Timestamp(combined_cumulative.index.min()).tz_localize(None)
data_max = pd.Timestamp(combined_cumulative.index.max()).tz_localize(None)

# ---- Sidebar controls ----
with st.sidebar:
    st.header("⚙️ Controls")

    selected_assets = st.multiselect(
        "Select series:",
        options=available_assets,
        default=available_assets[:3] if len(available_assets) >= 3 else available_assets,
        key="assets_select",
    )

    range_mode = st.selectbox(
        "Choose a date range",
        [
            "Custom (slider)",
            "Past Week",
            "Past Month",
            "Past 3 Months",
            "Past 6 Months",
            "Past Year",
            "Past 2 Years",
            "All Data",
        ],
        index=0,
        key="range_mode",
    )

    # ✅ Soustraction séquentielle des offsets (fixe l'erreur DateOffset)
    def offset_from_anchor(anchor, *, weeks=0, months=0, years=0) -> pd.Timestamp:
        res = pd.Timestamp(anchor).tz_localize(None)
        if weeks:
            res = res - pd.DateOffset(weeks=weeks)
        if months:
            res = res - pd.DateOffset(months=months)
        if years:
            res = res - pd.DateOffset(years=years)
        return pd.Timestamp(res).tz_localize(None)

    if range_mode == "Custom (slider)":
        start_ts, end_ts = st.slider(
            "Date range (drag the handles)",
            min_value=data_min.to_pydatetime(),
            max_value=data_max.to_pydatetime(),
            value=(data_min.to_pydatetime(), data_max.to_pydatetime()),
            format="YYYY-MM-DD",
            key="date_slider",
        )
        start_ts = pd.Timestamp(start_ts).tz_localize(None)
        end_ts = pd.Timestamp(end_ts).tz_localize(None)
    elif range_mode == "Past Week":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, weeks=1)
    elif range_mode == "Past Month":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, months=1)
    elif range_mode == "Past 3 Months":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, months=3)
    elif range_mode == "Past 6 Months":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, months=6)
    elif range_mode == "Past Year":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, years=1)
    elif range_mode == "Past 2 Years":
        end_ts = data_max
        start_ts = offset_from_anchor(data_max, years=2)
    else:  # "All Data"
        start_ts, end_ts = data_min, data_max

# Garde-fous
if start_ts > end_ts:
    start_ts, end_ts = end_ts, start_ts
start_ts = max(start_ts, data_min)
end_ts   = min(end_ts, data_max)

if not selected_assets:
    st.warning("Select at least one series.")
    st.stop()

filtered_data = (
    combined_cumulative.loc[start_ts:end_ts, selected_assets]
    .dropna(how="all")
)

# ---- Ticker descriptions ----
ticker_descriptions = {
    "CPIAUCNS": "US Consumer Price Index (Inflation measure)",
    "GDP": "US Gross Domestic Product (Growth measure)",
    "ES=F": "S&P 500 Futures (Equities)",
    "ZN=F": "10-Year US Treasury Note Futures (Bonds)",
    "GC=F": "Gold Futures (Safe haven asset)",
    "CL=F": "Crude Oil Futures (Energy prices)",
    "ZW=F": "Wheat Futures (Agricultural commodity)",
    "DX=F": "US Dollar Index Futures (Currency strength)",
}

st.subheader("Selected Series & Descriptions")
for ticker in selected_assets:
    desc = ticker_descriptions.get(ticker, "No description available")
    st.markdown(f"**{ticker}** — {desc}")

# ---- Interactive Plot (Plotly) with hover ----
fig = go.Figure()

for i, col in enumerate(filtered_data.columns):
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data[col],
            mode="lines",
            name=col,
            line=dict(width=2, color=rose_pine_colors[i % len(rose_pine_colors)]),
            hovertemplate="<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Index: %{y:.3f}<extra></extra>",
        )
    )

fig.update_layout(
    title=dict(text="Cumulative Growth of Selected Series", x=0.0, font=dict(color="#e0def4", size=18)),
    hovermode="x unified",  # <- infobulle commune sous la souris
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0),
    paper_bgcolor="#191724",
    plot_bgcolor="#191724",
    font=dict(color="#e0def4"),
    margin=dict(t=60, r=10, b=40, l=60),
)

fig.update_xaxes(
    title_text="Date",
    gridcolor="#524f67",
    zeroline=False,
)
fig.update_yaxes(
    title_text="Index (base=1.0)",
    gridcolor="#524f67",
    zeroline=False,
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

# ---- Data preview ----
with st.expander("🔎 Data preview"):
    st.dataframe(filtered_data.tail(10), use_container_width=True)

# ---- Footer (intro en bas) ----
footer_md = """
<hr style="border-color:#2a273f; margin-top:2rem; margin-bottom:1rem;">
<div style="color:#e0def4;">
  <p><strong>finance_dashboard_pipeline.py</strong></p>
  <p>This script synthesizes the key lessons from the Python for Finance lectures:</p>
  <ul>
    <li>Download financial and macroeconomic data (yfinance + FRED)</li>
    <li>Save and reload data from CSV files</li>
    <li>Handle missing values correctly (forward fill, no interpolation)</li>
    <li>Compute arithmetic returns</li>
    <li>Compute cumulative compounded returns (growth indexes)</li>
    <li>Plot and save charts</li>
    <li>Write modular code (each function does one thing only)</li>
  </ul>
</div>
"""
st.markdown(footer_md, unsafe_allow_html=True)



# next steps : 
# build up streamlit more (get something more user fiendly, + plus add some financial info (depending on the last infos for each ticker ))
# clean the github repo 
# coorect the instructions to run 



