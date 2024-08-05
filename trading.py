import numpy as np
import matplotlib.pyplot as plt

def strategy_build(df):
    df['sma_9'] = df['Close'].rolling(window=9).mean()
    df['sma_20'] = df['Close'].rolling(window=20).mean()
    df.dropna(inplace=True)

    df['signal'] = np.where(df['sma_9'] > df['sma_20'], 1, 0)
    df['buy_signal'] = np.where(((df['signal'] ==1) & (df['signal'].shift(1)==0)), 1, 0)
    df['sell_signal'] = np.where(((df['signal'] ==0) & (df['signal'].shift(1)==1)), 1, 0)
    df['shifted_open'] = df['Open'].shift(-1)
    return df


def execute_trade(df, stop_loss_per=0.95, transaction_cost=0):
    strategy_build(df)
    df['buyprices'] = 0
    df['sellprices'] = 0
    df['returns'] = 0
    df['buyprices'] = df['buyprices'].astype('float64')
    df['sellprices'] = df['sellprices'].astype('float64')
    df['returns'] = df['returns'].astype('float64')

    position = 0

    for index, row in df.iterrows():
        if (position == 0) and (row.buy_signal == 1):
            buyprice = row.shifted_open * (1 + transaction_cost)
            df.at[index, 'buyprices'] = buyprice
            position = 1
        
        if (position == 1):
            # If we hit stop loss
            if (row.Low < buyprice * stop_loss_per):
                sellprice = buyprice * stop_loss_per
                df.at[index, 'sellprices'] = sellprice
                df.at[index, 'returns'] = (sellprice - buyprice) / buyprice  # Convert to percentage return
                position = 0
            
            # If you SMA gives sell signal
            elif (row.sell_signal == 1):
                sellprice = row.Close
                df.at[index, 'sellprices'] = sellprice
                df.at[index, 'returns'] = (sellprice - buyprice) / buyprice   # Convert to percentage return
                position = 0

    df = df.loc[(df['buyprices'] != 0) | df['sellprices'] != 0]
    return df

def plot_signals(df):

    buyprices=df['buyprices'].loc[(df['buyprices'] != 0)]
    sellprices=df['sellprices'].loc[(df['sellprices'] != 0)]
    # Plot the closing prices
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.55)

    # Plot the moving averages
    plt.plot(df.index, df['sma_9'], label='9-Day SMA', color='orange', alpha=0.85)
    plt.plot(df.index, df['sma_20'], label='20-Day SMA', color='brown', alpha=0.85)

    # Plot buy signals
    plt.scatter(buyprices.index, buyprices, marker='^', color='green', label='Buy Signal', alpha=1, s=50)

    # Plot sell signals
    plt.scatter(sellprices.index, sellprices, marker='v', color='red', label='Sell Signal', alpha=1, s=50)

    # Add title and labels
    plt.title('Stock Price with Buy and Sell Signals', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Price', fontsize=16)
    plt.legend()
    plt.grid()

    # Show the plot
    plt.tight_layout()
    plt.show()
    return