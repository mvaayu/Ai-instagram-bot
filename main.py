import os
import yfinance as yf
from openai import OpenAI

client = OpenAI()


def fetch_market_data():
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")

    close = round(data["Close"].iloc[-1], 2)
    open_price = round(data["Open"].iloc[-1], 2)

    change = round(close - open_price, 2)
    percent = round((change / open_price) * 100, 2)

    return close, change, percent


def generate_caption(close, change, percent):
    prompt = f"""
    Create a short Instagram caption.

    Rules:
    - Only facts
    - No stock advice
    - Neutral tone
    - Max 3 lines
    - Add emojis

    Data:
    NIFTY close {close}
    Change {change} ({percent}%)
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def main():
    print("🚀 Bot started")

    close, change, percent = fetch_market_data()

    caption = generate_caption(close, change, percent)

    print("\n📢 Generated Caption:\n")
    print(caption)


if __name__ == "__main__":
    main()
