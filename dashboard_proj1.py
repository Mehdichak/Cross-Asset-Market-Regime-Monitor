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
data = yf.download ("SPY", start="2000-01-01", end="2024-12-31")
print(data.head())    