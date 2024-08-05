from data import download_historical_data, data_summary,handle_missing_values,plot_cumulative_returns, plot_closing_prices
from datetime import date

symbol="BTC-USD"
start_date="2020-01-01"
end_date = date.today().strftime('%Y-%m-%d')
timeframe="1d"
