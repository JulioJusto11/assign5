import pandas as pd
import streamlit as st
import yfinance as yf

# Streamlit Page Setup
st.title("MSFT 5-Year Sharpe Ratio Analysis")

# Fixed parameters per instructions
ticker = "MSFT"
rf_monthly = 0.0025  # 0.25% per month risk-free rate

with st.spinner("Fetching historical data from Yahoo Finance..."):
    # Download monthly stock data for MSFT for the past 5 years
    data = yf.download(ticker, period="5y", interval="1mo", progress=False)

if not data.empty:
    # Safely extract the 'Close' prices for single or multi-index DataFrames
    if isinstance(data["Close"], pd.DataFrame):
        close_prices = data["Close"][ticker]
    else:
        close_prices = data["Close"]

    # Calculate monthly returns and drop initial NaN
    monthly_returns = close_prices.pct_change().dropna()

    # Calculate excess returns and standard deviation
    excess_returns = monthly_returns - rf_monthly
    mean_excess_return = excess_returns.mean()
    std_dev_return = monthly_returns.std()

    # Calculate Monthly Sharpe Ratio
    monthly_sharpe_ratio = mean_excess_return / std_dev_return

    # Display Metrics in Streamlit
    st.subheader(f"Results for {ticker}")
    st.metric(
        label="Monthly Sharpe Ratio (5-Year)",
        value=f"{monthly_sharpe_ratio:.3f}",
    )

    # Optional: Display monthly performance metric details
    with st.expander("View Calculation Details"):
        st.write(f"- **Stock Ticker:** {ticker}")
        st.write(f"- **Risk-Free Rate:** {rf_monthly * 100:.2f}% / month")
        st.write(f"- **Mean Monthly Return:** {monthly_returns.mean() * 100:.2f}%")
        st.write(f"- **Monthly Volatility (Std Dev):** {std_dev_return * 100:.2f}%")
else:
    st.error("Unable to retrieve stock data for MSFT. Please try again later.")
