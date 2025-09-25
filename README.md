**# Cross-Asset-Market-Regime-Monitor
MSc in Financial Markets and Investments Python Programming for Finance
**🌍 Cross-Asset Market Regime Dashboard
🔎 Introduction

This repository contains the foundations of a cross-asset monitoring tool developed in the context of the Python Programming for Finance course (MSc Financial Markets & Investments, Skema Business School).

The project is progressively moving from a data pipeline (finance_dashboard_pipeline.py) to a fully interactive Streamlit dashboard.
At its core, the tool combines:

Macroeconomic indicators (growth & inflation)

Financial assets (equities, bonds, commodities, currencies)

Visualization methods to better understand market regimes

🎯 Objectives

The dashboard is designed to:

Track the performance of major asset classes across different regimes

Monitor indicators for growth, inflation, volatility, and yields

Explore term structures (futures) and yield curves (bonds)

Provide a clean interface for traders, portfolio managers, and students

👤 Who Is This For?

Practitioners (portfolio managers, traders) needing a quick cross-asset overview

Academics & students exploring Python tools for financial markets

Developers curious about building financial dashboards with Streamlit

✅ Features Implemented

Data acquisition

CPI & GDP from FRED

Asset prices (S&P 500, Treasuries, Gold, Oil, Wheat, Dollar Index) from Yahoo Finance

Preprocessing

Save/reload datasets as CSV

Forward-fill missing values

Compute arithmetic returns & compounded growth indices

Visualization

Line plots for cumulative growth of macro indicators

Line plots for cumulative growth of financial assets

🚧 Roadmap

Planned enhancements:

Futures term structure curves (equities, commodities, USD index)

Yield curve visualizations (US Treasuries, German Bunds)

Heatmaps for cross-asset performance comparisons

Interactive filters (time periods, regimes, asset groups)

Deployment on a server with daily auto-updates

⚙️ Technical Setup
Requirements

Python ≥ 3.11

Packages:

pip install pandas numpy matplotlib yfinance pandas_datareader streamlit

How to Run

Clone the repository:

git clone https://github.com/your-username/Cross-Asset-Market-Regime-Monitor.git
cd Cross-Asset-Market-Regime-Monitor


Run the pipeline script (data prep + plots):

python finance_dashboard_pipeline.py


Start the interactive dashboard:

streamlit run streamlit_app.py


Open the app in your browser at http://localhost:8501
.

📢 Project Status

Data pipeline: done

Basic visualizations: done

Streamlit UI: in progress

Deployment: not yet

📌 Notes

At this stage the focus is data reliability.
The dashboard layer will be progressively enriched with interactivity and regime analysis tools.
