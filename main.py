import yfinance as yf

def fetch_market_data():
    nifty = yf.Ticker("^NSEI")

    data = nifty.history(period="1d")

    close = round(data["Close"].iloc[-1], 2)
    open_price = round(data["Open"].iloc[-1], 2)

    change = round(close - open_price, 2)
    percent = round((change / open_price) * 100, 2)

    print("📊 Market Recap")
    print(f"NIFTY Close: {close}")
    print(f"Change: {change} ({percent}%)")

def main():
    print("🚀 Bot started")
    fetch_market_data()

if __name__ == "__main__":
    main()
