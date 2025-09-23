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

#Data download 
def data_download(ticker,filename):
    data = yf.download(ticker)['Close']
    data.to_csv(filename)

ticker_filename={
    "SPY":"spy.csv",
    "DX-Y.NYB": "usd.csv",
    "GC=F":"gold.csv",
    "WTI":"wti.csv",
    "^TNX": "bonds.csv"
}

# create a mapping to avoid special caracters in ticker 
sanitized_ticker = {ticker:filename.replace('.csv','') for ticker,filename in ticker_filename.items()}




for ticker,filename in ticker_filename.items():
    data_download(ticker,filename)

# Sanity Checks 

#  fct Check for missisng values 
def check_na(data):
    null_sum = data.isna().sum()
    null_percentage = null_sum/len(data)
    print("ratio of missing values : {null_percentage}")

# fct to fill missing values 
def  fill_missing_values(df): 
    '''
    Fill missing values using ffill method, 
    input is the data frame 
    output the dataframe 
    '''
    df= df.ffill().dropna()
    return df


# fct to plot & save the figures png 
def plot_df(ticker):

    data = pd.read_csv(ticker_filename[ticker])
    plt.figure()
    plt.title(sanitized_ticker[ticker])
    plt.plot(data.index,data[ticker])
    plt.savefig(sanitized_ticker[ticker]+ '.png')

# create a loop that does everything for each ticker 
for ticker in ticker_filename.keys() : 
    print (f"checking {ticker}")
    data = pd.read_csv(ticker_filename[ticker],index_col=0,parse_dates= True)
    check_na(data)
    print("")
    data=fill_missing_values(data)
    plot_df(ticker)










# checking with only spy (to verify the process & have clear idea)
spy = pd.read_csv("spy.csv", index_col=0, parse_dates=True)# ['SPY'].pct_change() +1).cumprod()
check_na(spy)
fill_missing_values(spy)
plot_df(spy)





# # Check for missing values 

# # missing_values = data.isnull().sum #number is zero 
# # Plot the data 
# spy.plot(label='SPY')
# plt .ylabel ("SPY closing price")
# plt.title("SPY Closing price over time")
# plt.yscale('log')


# #forex using USD index 

# usd= (yf.download("DX-Y.NYB", start=spy.index.min())['Close'].pct_change() +1).cumprod
# usd['DX-Y.NYB'].plot(label='USD INDEX')
# plt.legend()
# plt.show() 


# -------future work ---------
# write a function to deal with missing values 
#scale the data
#write small functions for each of the data preprocessing steps and then one main function to call them all 
# create a function that does plotting in a systematic way
# inchallah use streamlit 
