# dashboard for equity(s&p), forex(usd), commo(gold,crude oil, wheat,) bonds (inflation-linked bonds)
# data abaout growth inflation volatily & yield 
#as far as the data are available 
#widget to choose the window of time 


#import math
#from datetime import date, datetime, timedelta
#from typing import Dict, List, Optional

import yfinance as yf 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#import plotly.express as px
#import plotly.graph_objects as go
#import streamlit as st


# getting the data for SPY 
  
spy_df = yf. download ("SPY ") # full history by default
spy = spy_df [["Close"]]. rename ( columns ={"Close": "SPY_Close"})
print ("SPY head:")
print (spy. head ())
print ("SPY date range :", spy. index .min () , " ->", spy. index .max ())

# saving & reloading data 
# 2. Save and reload locally ( robustness )
spy.to_csv ("spy_data.csv")
spy_from_file = pd.read_csv ("spy_data .csv", index_col =0, parse_dates =
True )
print (" Index types :", type (spy. index ), type ( spy_from_file . index ))
# 3. Validate data na checking 
missing_counts = spy.isna().sum()
print (" Missing counts :\n", missing_counts )
# this part is very is we need to, verify missisng values, if we have some we can try to fill with fillna() or interpolation


# 4. Quick plot (SPY only )
spy.plot(y="SPY_Close", title="SPY Close (full history)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# 6. Fetch DXY and EURUSD

#(DXY)
dxy_df = yf.download("DX-Y.NYB")   # full history by défaut
dxy = dxy_df[["Close"]].rename(columns={"Close": "DXY_Close"})
eurusd_df = yf.download("EURUSD=X")
eurusd = eurusd_df[["Close"]].rename(columns={"Close": "EURUSD_Close"})
print("Fetched series:", list([c for c in [spy.columns, dxy.columns, eurusd.columns]]))

# 7. Returns and cumulative returns

def pct_to_cumret(series):
    """
    Convert a price series to cumulative returns.
    Starts at 1.0, grows over time.
    """
    r = series.pct_change()        # rendement simple : (P_t - P_{t-1}) / P_{t-1}
    cumret = (1.0 + r).cumprod()   # cumul = produit des (1 + rendement)
    cumret.iloc[0] = 1.0           # normalisation : commence à 1.0
    return cumret

# Aplication on  DXY et EURUSD
dxy_cum = pct_to_cumret(dxy["DXY_Close"])
eurusd_cum = pct_to_cumret(eurusd["EURUSD_Close"])
# 8. Align multiple series safely

# dictionnaire 
series_map = {
    "SPY_Close": spy["SPY_Close"],
    "DXY_Close": dxy["DXY_Close"],
    "EURUSD_Close": eurusd["EURUSD_Close"]
}

# Trouver la première date valide de chaque série (dropna)
first_dates = [s.dropna().index.min() for s in series_map.values()]

#  point de départ commun
common_start = max(first_dates)

# concat in one DataFrame
multi = pd.concat(series_map, axis=1, join="outer")
aligned = multi[multi.index >= common_start]

# Vérification
print("Common start date:", common_start)
print(aligned.head())


# 9. Normalize all series to cumulative returns (step by step with a loop)

# Create an empty DataFrame to store cumulative returns
multi_cum = pd.DataFrame(index=aligned.index)
#  This will hold the normalized cumulative return series for each asset.

# Loop through each column of the aligned DataFrame
for col in aligned.columns:
    # Compute the daily percentage change (simple return)
    daily_return = aligned[col].pct_change()
    # This gives the day-to-day % change, e.g. (P_t - P_{t-1}) / P_{t-1}

    # Compute the cumulative product of (1 + daily return)
    cum_return = (1 + daily_return).cumprod()
    # This simulates investing 1 unit at the start and growing over time.

    # Force the first value to 1.0 (normalize starting point)
    cum_return.iloc[0] = 1.0
    # Ensures comparability across all series.

    # Store the result in the DataFrame under the same column name
    multi_cum[col] = cum_return
    # Adds the new cumulative return series for this asset.

# Display first 5 rows of the result
print(multi_cum.head())
#  Check that all series start at 1.0 and evolve consistently.

# 10. Plot aligned series (prices and cumrets)

# Plot aligned prices (SPY, DXY, EURUSD)
aligned.plot(title="Aligned Prices (SPY, DXY, EURUSD)")
# → Draws each column of aligned on the same chart (indexed by Date).
plt.xlabel("Date")      
plt.ylabel("Price")     
plt.tight_layout()      # → Avoids label/title clipping
plt.show()          

# Plot aligned cumulative returns (normalized to 1.0)
multi_cum.plot(title="Aligned Cumulative Returns (SPY, DXY, EURUSD)")
#  Plots the normalized growth curves starting at 1.0 for all series.
plt.xlabel("Date")                         
plt.ylabel("Cumulative Return (base = 1)") 
plt.tight_layout()                         
plt.show()    

# 11. Save outputs

# Save aligned prices so you can reuse without re-downloading
aligned.to_csv("aligned_prices.csv")
# → Exports the aligned price series (same dates across all columns).
multi_cum.to_csv("aligned_cumrets.csv")
# → Exports the normalized cumulative return series.

print("Saved aligned prices and cumulative returns.")

#~ second session 
# adding ten years tresuries for bonds (^tnx)
# adding ticker for commodities (gold) (GD=f), ticker for the wheat (zw=f) 


#crude oil (how to )
wti=yf.download("WTI") ['Close']
wti=(pd.read_csv("wti_data.csv"),index_col=0,parse_dates=True)['wti'].pct_change()+1.cumprod()




