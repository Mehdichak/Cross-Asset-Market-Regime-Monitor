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
