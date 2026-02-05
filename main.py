import yfinance as yf
from datetime import datetime

TOPICS = [
    "DAILY_PERFORMANCE",
    "WEEKLY_PERFORMANCE",
    "MONTHLY_RANGE",
    "GREEN_RED_DAYS",
    "BEST_WORST_DAY"
]

def choose_topic():
    today = datetime.utcnow().date()
    index = today.toordinal() % len(TOPICS)
    return TOPICS[index]

def fetch_nifty_data(days=30):
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period=f"{days}d")
    return data

def generate_topic_data(topic, data):
    if data.empty:
        return None

    if topic == "DAILY_PERFORMANCE":
        last = data.iloc[-1]
        prev = data.iloc[-2]
        pct = round(((last["Close"] - prev["Close"]) / prev["Close"]) * 100, 2)
        return f"NIFTY 50 moved {pct}% in the last session."

    if topic == "WEEKLY_PERFORMANCE":
        start = data.iloc[-6]["Close"]
        end = data.iloc[-1]["Close"]
        pct = round(((end - start) / start) * 100, 2)
        return f"NIFTY 50 changed {pct}% over the last 5 trading sessions."

    if topic == "MONTHLY_RANGE":
        high = round(data["High"].max(), 2)
        low = round(data["Low"].min(), 2)
        return f"In the last 30 days, NIFTY 50 ranged between {low} and {high}."

    if topic == "GREEN_RED_DAYS":
        green = (data["Close"] > data["Open"]).sum()
        red = (data["Close"] < data["Open"]).sum()
        return f"Out of the last 30 sessions, NIFTY closed green {green} times and red {red} times."

    if topic == "BEST_WORST_DAY":
        best = round(data["Close"].pct_change().max() * 100, 2)
        worst = round(data["Close"].pct_change().min() * 100, 2)
        return f"Best single-day move in last 30 days: {best}%. Worst: {worst}%."

def main():
    topic = choose_topic()
    data = fetch_nifty_data()
    content = generate_topic_data(topic, data)

    print({
        "topic": topic,
        "content": content
    })

if __name__ == "__main__":
    main()
