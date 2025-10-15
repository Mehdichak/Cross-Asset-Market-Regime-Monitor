# 🌍 Cross-Asset Market Regime Dashboard

A work-in-progress project to monitor **cross-asset market regimes** by combining macroeconomic indicators and financial asset data.  
Developed as part of the *Python Programming for Finance* course (MSc Financial Markets & Investments, Skema Business School).

---

## 📌 Overview
This repository provides a Python pipeline and Streamlit dashboard for analyzing:
- **Macroeconomic indicators** (e.g., CPI, GDP from FRED)  
- **Financial assets** (Equities, Bonds, Commodities, Dollar Index from Yahoo Finance)  

The workflow covers **data collection**, **preprocessing**, **return computations**, and **basic visualizations**.  
Future development will expand the interactive Streamlit dashboard with **filters, yield curves, and term structures**.

---

## 🎯 Features
### ✅ Implemented
- Download and save macroeconomic + financial data to CSV  
- Handle missing values with forward fill  
- Compute arithmetic and cumulative compounded returns  
- Generate plots for cumulative growth  

### 🚧 Planned
- Term structures for futures  
- Yield curves for bonds (US, Germany)  
- Heatmaps and cross-asset comparisons  
- Streamlit filters for time periods, regimes, and asset classes  
- Automated daily updates  

---

## ⚙️ Installation

Clone the repository:
```bash
git clone https://github.com/your-username/cross-asset-dashboard.git
cd cross-asset-dashboard


Create and activate a virtual environment (Python ≥ 3.11):
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate    # Windows


Install dependencies:
pip install -r requirements.txt

If you don’t have requirements.txt, install directly:
pip install pandas numpy matplotlib yfinance pandas_datareader streamlit

##  Running
afterinstallation:
run program 
typeinterminal streamlit run profcode-1.py
withoutinsallation:  https://cross-asset-market-regime-monitor-xntupsnjdqhnfnjksmpfgv.streamlit.app/



