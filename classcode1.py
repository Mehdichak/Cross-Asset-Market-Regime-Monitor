# class code folowing based on teams reunions 
#session 1 & 2 
# to move from one one branch to other, git checkout name of branch 
#Dashboard with equity (SPY), forex(USD), commodities (Gold , crude oil , wheat) , bonds (inflation-linkedbonds) 

#import streamlit as st 
import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt 

# Getting the data for spy (daily)
#closing prices only 
#data = yf.dowload("SPY")['Close']
# data.to_csv("spy_data.csv")
#print (data.index)

spy = (pd.read_csv("spy_data.csv", index_col=0, parse_dates=True)['SPY'].pct_change() +1).cumprod()

# Check for missing values 

# missing_values = data.isnull().sum #number is zero 
# Plot the data 
spy.plot(label='SPY')
plt .ylabel ("SPY closing price")
plt.title("SPY Closing price over time")
plt.yscale('log')


#forex using USD index 

usd= (yf.download("DX-Y.NYB", start=spy.index.min())['Close'].pct_change() +1).cumprod
usd['DX-Y.NYB'].plot(label='USD INDEX')
plt.legend()
plt.show() 
