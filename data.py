import pandas as pd
from IPython.display import display
from extra.data_fetch import download_historical_data
import matplotlib.pyplot as plt
import yfinance as yf

def download_historical_data(symbol,start_date,end_date,timeframe="1d"):
    data=yf.download(symbol,start=start_date,end=end_date,interval=timeframe)
    return data

def data_summary(df):
    rows, columns = df.shape
    print(f"Data Size: {rows} rows, {columns} columns")
    
    stats_df = pd.DataFrame({'Mean': df.mean(), 'Median': df.median(), 'Std': df.std()})

    # Transpose the DataFrame to match your desired format
    stats_df = stats_df.T

    # Assuming missing_values is a Series calculated from df
    missing_values = df.isna().sum()

    # Convert missing_values Series to DataFrame and transpose it
    missing_values_df = pd.DataFrame(missing_values).T

    # Rename the index to match the stats_df format
    missing_values_df.index = ['Missing_values']

    # Append missing_values_df to stats_df
    stats_df = pd.concat([stats_df, missing_values_df])
    display(stats_df)
    return

def handle_missing_values(df,method='ffill'):
    if method == 'ffill':
        df.fillna(method='ffill', inplace=True)
    elif method == 'bfill':
        df.fillna(method='bfill', inplace=True)
    elif method == 'interpolate':
        df.interpolate(method='linear', inplace=True)
    
    # df.fillna(df.rolling(window=3, min_periods=1).mean(), inplace=True)  # Adjust window as needed
    return df

def plot_cumulative_returns(df,symbol):
    # Fetch historical data for the stock and the index
    start_date_index=df.index.min()
    end_date_index=df.index.max()
    index_data = download_historical_data("^NSEI", start_date_index, end_date_index)
    # handle_missing_values(df)
    # handle_missing_values(index_data)
    
    # Calculate daily returns
    stock_returns = df['Adj Close'].pct_change()
    index_returns = index_data['Adj Close'].pct_change()
    
    # Calculate cumulative returns
    stock_cumulative_returns = (1 + stock_returns).cumprod() - 1
    index_cumulative_returns = (1 + index_returns).cumprod() - 1
    
    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(stock_cumulative_returns, label=f'{symbol} Cumulative Returns')
    plt.plot(index_cumulative_returns, label='Nifty50 Cumulative Returns', color='red')
    plt.title(f'{symbol} vs Nifty50 Cumulative Returns', fontsize=20)
    plt.xlabel('Date',fontsize=16)
    plt.ylabel('Cumulative Returns',fontsize=20)
    plt.legend()

    plt.tight_layout()
    plt.grid()
    plt.show()

    return