import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_returns(df):
    returns=df['returns'][(df['returns'] != 0)]
    return returns

def calculate_cumulative_returns(df):
    cum_returns = ((1 + df['returns'][(df['returns'] != 0)]).cumprod() - 1)
    cum_returns.dropna(inplace=True)
    return cum_returns

def calculate_max_drawdown(cumulative_returns):
    cumulative_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / cumulative_max - 1
    max_drawdown = drawdown.min()
    print("Max Drowdown is:",max_drawdown*100,"%")
    return

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    excess_returns = returns - risk_free_rate
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
    print("Sharpe Ratio is:",sharpe_ratio)
    return

def calculate_sortino_ratio(returns, risk_free_rate=0):
    excess_returns = returns - risk_free_rate
    downside_returns = excess_returns[excess_returns < 0]
    sortino_ratio = np.mean(excess_returns) / np.std(downside_returns)
    print("Sortino Ratio is:",sortino_ratio)
    return 

def calculate_hit_ratio(returns):
    profitable_trades = returns[returns > 0]
    hit_ratio = len(profitable_trades) / len(returns)
    print("Hit Ratio is:",hit_ratio)
    return 

def generate_monthly_returns_heatmap(df):
    data_monthly = df.resample('ME').sum()

    # Calculate the monthly returns
    monthly_returns = data_monthly['returns']

    # Convert monthly returns to a pandas DataFrame
    monthly_returns_df = pd.DataFrame(monthly_returns)

    # Pivot the DataFrame to create a matrix of monthly returns by year and month
    monthly_returns_matrix = monthly_returns_df.pivot_table(values='returns', index=monthly_returns_df.index.year, columns=monthly_returns_df.index.month)

    # Set the column names to the month names
    monthly_returns_matrix.columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Calculate the sum of monthly returns for each year
    yearly_returns = monthly_returns_df.groupby(monthly_returns_df.index.year)['returns'].sum()

    # Add the yearly returns to the matrix as a new column
    monthly_returns_matrix['Yearly'] = yearly_returns

    # Set the font scale
    sns.set(font_scale=1.2)

    # Plot the heatmap using seaborn
    plt.figure(figsize=(14, 12))
    sns.heatmap(monthly_returns_matrix, annot=True, cmap='RdYlGn', center=0, fmt='.2%', cbar=False)
    plt.title('Stock Monthly and Yearly Returns by Year and Month', fontsize=20)
    plt.xlabel('Month', fontsize=16)
    plt.ylabel('Year', fontsize=16)

    plt.tight_layout()
    plt.show()