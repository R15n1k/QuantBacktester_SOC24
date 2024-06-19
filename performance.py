from data_fetch import download_historical_data
import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np

symbol="RELIANCE.NS"
start_date="2024-06-01"
end_date="2024-06-18"
timeframe="1d"

def plot_closing_prices(symbol,start_date,end_date,timeframe):

    df=download_historical_data(symbol,start_date,end_date,timeframe)
    plt.figure(figsize=(10,6))

    plt.plot(df["Date"],df["Close"],marker="o")

    plt.xlabel("Dates",fontsize=16)
    plt.ylabel("Closing Price",fontsize=16)
    plt.title(f"Closing Price of {symbol}",fontsize=20,fontweight="bold")

    plt.xticks(pd.date_range(df["Date"].min(),df["Date"].max()),rotation=60)
    plt.tight_layout()
    plt.show()
