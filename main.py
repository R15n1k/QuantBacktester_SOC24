from performance import plot_closing_prices
from data_fetch import download_historical_data

# import pandas as pd
# import matplotlib.pyplot as py
# import numpy as np

symbol="BTC-USD"
start_date="2024-06-01"
end_date="2024-06-18"
timeframe="1d"


plot_closing_prices(symbol,start_date,end_date,timeframe)



