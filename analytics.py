import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# List of stock symbols to track
symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

def fetch_stock_data(symbols):
    records = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1h")
        if not hist.empty:
            latest = hist.tail(1)
            record = {
                "Symbol": symbol,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Open": float(latest["Open"]),
                "Close": float(latest["Close"]),
                "High": float(latest["High"]),
                "Low": float(latest["Low"]),
                "Volume": int(latest["Volume"]),
                "Percent Change": round((latest["Close"].iloc[0] - latest["Open"].iloc[0]) / latest["Open"].iloc[0] * 100, 2)
            }
            records.append(record)
    return pd.DataFrame(records)

def save_summary(df):
    output_path = "data/daily_summary.csv"

    if os.path.exists(output_path):
        existing = pd.read_csv(output_path)
        updated = pd.concat([existing, df], ignore_index=True)
        updated.drop_duplicates(subset=["Symbol", "Date"], inplace=True)
        updated.sort_values(by=["Date", "Symbol"], ascending=[True, True], inplace=True)
        updated.to_csv(output_path, index=False)
        print(f"Appended new data to {output_path}")
    else:
        df.to_csv(output_path, index=False)
        print(f"Created new file {output_path}")

if __name__ == "__main__":
    df = fetch_stock_data(symbols)
    if not df.empty:
        save_summary(df)
    else:
        print("No data fetched.")

