import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(page_title="Stock Analysis Dashboard", page_icon="📈", layout="wide")

st.title("📈 Stock Price & Sharpe Ratio Dashboard")
st.markdown("Analyze 5-year historical performance, average closing prices, and monthly Sharpe Ratios for any stock.")

# Sidebar Controls
st.sidebar.header("User Inputs")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper().strip()
rf_annual = st.sidebar.number_input("Annual Risk-Free Rate (%)", value=3.0, step=0.25, min_value=0.0) / 100
rf_monthly = rf_annual / 12  # Convert annual rate to monthly

if st.sidebar.button("Run Analysis", type="primary") or ticker:
    st.subheader(f"Results for **{ticker}**")
    
    with st.spinner("Fetching data from Yahoo Finance..."):
        # Fetch 5 years of daily data for overall average calculation & chart
        stock_obj = yf.Ticker(ticker)
        daily_data = stock_obj.history(period="5y")
        
        # Fetch monthly data for Sharpe Ratio calculation
        monthly_data = yf.download(ticker, period="5y", interval="1mo", progress=False)

    if not daily_data.empty and not monthly_data.empty:
        # -------------------------------------------------------------
        # Code 2 Logic: 5-Year Average Closing Price
        # -------------------------------------------------------------
        overall_average = daily_data['Close'].mean()

        # -------------------------------------------------------------
        # Code 1 Logic: Monthly Sharpe Ratio
        # -------------------------------------------------------------
        # Ensure correct column reference whether single or multi-index DataFrame is returned
        if isinstance(monthly_data['Close'], pd.DataFrame):
            close_prices = monthly_data['Close'][ticker]
        else:
            close_prices = monthly_data['Close']
            
        monthly_returns = close_prices.pct_change().dropna()
        excess_returns = monthly_returns - rf_monthly
        mean_excess_return = excess_returns.mean()
        std_dev_return = monthly_returns.std()

        # Calculate Monthly Sharpe Ratio
        if std_dev_return != 0:
            monthly_sharpe_ratio = mean_excess_return / std_dev_return
        else:
            monthly_sharpe_ratio = 0.0

        # Annualized Sharpe Ratio approximation (Optional metric)
        annualized_sharpe = monthly_sharpe_ratio * (12 ** 0.5)

        # -------------------------------------------------------------
        # Display Results in Streamlit
        # -------------------------------------------------------------
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="5-Year Average Price", value=f"${overall_average:.2f}")
            
        with col2:
            st.metric(label="Monthly Sharpe Ratio", value=f"{monthly_sharpe_ratio:.3f}")
            
        with col3:
            st.metric(label="Annualized Sharpe Ratio", value=f"{annualized_sharpe:.3f}")

        # Display Historical Chart
        st.write("---")
        st.subheader("5-Year Price History")
        st.line_chart(daily_data['Close'])

        # Detailed breakdown in expander
        with st.expander("Show Detailed Calculation Metrics"):
            st.write(f"- **Monthly Risk-Free Rate Used:** {rf_monthly*100:.4f}%")
            st.write(f"- **Mean Monthly Excess Return:** {mean_excess_return*100:.2f}%")
            st.write(f"- **Monthly Standard Deviation:** {std_dev_return*100:.2f}%")
            
    else:
        st.error(f"No data found for ticker **'{ticker}'**. Please check the symbol and try again.")
