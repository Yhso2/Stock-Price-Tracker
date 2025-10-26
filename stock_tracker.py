import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

# App title
st.set_page_config(page_title="Stock Price Tracker", page_icon="📈")
st.title("📊 Simple Stock Price Tracker")
st.write("Enter a stock ticker symbol (e.g., AAPL, GOOGL, TSLA) to see its price and chart.")

# User input
ticker = st.text_input("Stock Ticker", value="AAPL").upper()

if ticker:
    try:
        # Fetch company info and data
        stock = yf.Ticker(ticker)
        info = stock.info

        # Validate if valid ticker
        if 'currentPrice' not in info and 'regularMarketPrice' not in info:
            st.error(f"❌ '{ticker}' is not a valid stock ticker. Please try again.")
        else:
            company_name = info.get('longName', ticker)
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            currency = info.get('currency', 'USD')

            # Display summary
            st.subheader(f"{company_name} ({ticker})")
            st.metric(label="Current Price", value=f"{current_price} {currency}")

            # Fetch historical data (last 30 days)
            end_date = datetime.today()
            start_date = end_date - timedelta(days=30)
            hist = stock.history(start=start_date, end=end_date)

            if not hist.empty:
                # Create candlestick or line chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=hist['Close'],
                    mode='lines+markers',
                    name='Close Price',
                    line=dict(color='royalblue', width=2)
                ))
                fig.update_layout(
                    title=f"{ticker} Price (Last 30 Days)",
                    xaxis_title="Date",
                    yaxis_title=f"Price ({currency})",
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No historical data available.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Data from Yahoo Finance via yfinance • Not financial advice")