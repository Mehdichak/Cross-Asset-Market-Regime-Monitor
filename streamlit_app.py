import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 

# to run streamlit : streamlit run streamlit_app.py
# to stop press control c 
# documentation for streamlit.  https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect

# plot le site & set the title 
# plot le site & set the title 
title="Cross Asset Regime Monitor"
st.set_page_config(title,layout="wide")
st.title(title)


# prepare the data
data = pd.read_csv("alL_data.csv",index_col=0,parse_dates=True)
data = data.ffill().dropna()
returns = data.pct_change()
cum_returns = (1+returns).cumprod()
assets = cum_returns.columns

#setting the dates 
min_date = cum_returns.index[0]
max_date = cum_returns.index[-1]


# preparing the sidebar selector 
with st.sidebar:
    selected_assets = st.multiselect("Please select your assets",assets)
    range_start, range_end = st.date_input("Date range",value=(min_date,max_date))



# plot all data first
fig1 = plt.figure(figsize=(10,5)) #create an empty figure to put the plot in it 
plt.plot(cum_returns,label=cum_returns.columns)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title(title)

st.dataframe(cum_returns) # show the data
st.pyplot(fig1)

#plot the selected assets
fig2 = plt.figure(figsize=(10,5))

plt.plot(cum_returns[selected_assets],label=cum_returns[selected_assets].columns)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title("Selected Assets")
st.pyplot(fig2)




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
