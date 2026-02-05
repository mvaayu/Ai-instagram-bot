import yfinance as yf

def fetch_nifty_snapshot():
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="5d")

    if data.empty:
        return None

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    close = round(latest["Close"], 2)
    prev_close = round(prev["Close"], 2)

    pct_change = round(((close - prev_close) / prev_close) * 100, 2)

    return {
        "index": "NIFTY 50",
        "close": close,
        "pct_change": pct_change
    }

if __name__ == "__main__":
    snapshot = fetch_nifty_snapshot()
    print(snapshot)
print("🚀 Bot is alive and running successfully!")
