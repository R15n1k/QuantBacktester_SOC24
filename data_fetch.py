import yfinance as yf

def download_historical_data(symbol,start_date,end_date,timeframe="1d"):
    data=yf.download(symbol,start=start_date,end=end_date,interval=timeframe)
    data.reset_index(inplace=True)
    return data
