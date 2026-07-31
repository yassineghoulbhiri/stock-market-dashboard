
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")
st.title("📊 Stock Market Analysis Dashboard")

# Sidebar controls
st.sidebar.header("Settings")
tickers = st.sidebar.multiselect(
    "Choose stocks",
    ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "NVDA"],
    default=["AAPL", "MSFT", "AMZN", "GOOGL"]
)
start_date = st.sidebar.date_input("Start date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End date", pd.to_datetime("today"))

if tickers:
    data = yf.download(tickers, start=start_date, end=end_date)["Close"]

    st.subheader("Raw Closing Prices")
    st.line_chart(data)

    st.subheader("Normalized Comparison (Base = 100)")
    normalized = data / data.iloc[0] * 100
    st.line_chart(normalized)

    st.subheader("Moving Averages")
    selected_stock = st.selectbox("Pick a stock for moving average view", tickers)
    ma_data = pd.DataFrame({
        selected_stock: data[selected_stock],
        "MA20": data[selected_stock].rolling(20).mean(),
        "MA50": data[selected_stock].rolling(50).mean()
    })
    st.line_chart(ma_data)

    st.subheader("Daily Returns Volatility (Box Plot)")
    returns = data.pct_change()
    fig, ax = plt.subplots(figsize=(10,5))
    returns.plot(kind="box", ax=ax)
    st.pyplot(fig)

    st.subheader("Summary Stats")
    st.dataframe(returns.describe())
else:
    st.warning("Select at least one stock from the sidebar.")
