import yfinance as yf
import pandas as pd
# Define the ticker and risk-free rate
ticker = 'AAPL'
rf_monthly = 0.0025 # 0.25% per month
# Download monthly stock price data for the past 5 years
data = yf.download(ticker, period='5y', interval='1mo')
close_prices = data['Close'][ticker]
# Calculate monthly returns
monthly_returns = close_prices.pct_change().dropna()
# Calculate average excess return and standard deviation of returns
excess_returns = monthly_returns - rf_monthly
mean_excess_return = excess_returns.mean()
std_dev_return = monthly_returns.std()
# Calculate the Monthly Sharpe Ratio
monthly_sharpe_ratio = mean_excess_return / std_dev_return
print()
print()
print(f"Ticker: {ticker}")
print(f"Monthly Sharpe Ratio: {monthly_sharpe_ratio:.3f}")
