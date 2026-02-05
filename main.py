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
    return ticker.history(period=f"{days}d")

def generate_fact(topic, data):
    if topic == "DAILY_PERFORMANCE":
        last, prev = data.iloc[-1], data.iloc[-2]
        pct = round(((last["Close"] - prev["Close"]) / prev["Close"]) * 100, 2)
        return pct

    if topic == "WEEKLY_PERFORMANCE":
        start, end = data.iloc[-6]["Close"], data.iloc[-1]["Close"]
        return round(((end - start) / start) * 100, 2)

    if topic == "MONTHLY_RANGE":
        return round(data["Low"].min(), 2), round(data["High"].max(), 2)

    if topic == "GREEN_RED_DAYS":
        green = (data["Close"] > data["Open"]).sum()
        red = (data["Close"] < data["Open"]).sum()
        return green, red

    if topic == "BEST_WORST_DAY":
        return (
            round(data["Close"].pct_change().max() * 100, 2),
            round(data["Close"].pct_change().min() * 100, 2)
        )

def generate_script(topic, fact):
    if topic == "DAILY_PERFORMANCE":
        return [
            "Here’s a quick market recap.",
            f"NIFTY 50 moved {fact} percent in the last session.",
            "This reflects the market’s short-term movement."
        ]

    if topic == "WEEKLY_PERFORMANCE":
        return [
            "Let’s look at the last five trading days.",
            f"NIFTY 50 changed by {fact} percent over the week.",
            "That’s the broader weekly market trend."
        ]

    if topic == "MONTHLY_RANGE":
        low, high = fact
        return [
            "Looking at the past month.",
            f"NIFTY 50 traded between {low} and {high}.",
            "This shows the recent trading range."
        ]

    if topic == "GREEN_RED_DAYS":
        green, red = fact
        return [
            "Market consistency check.",
            f"NIFTY closed green {green} days and red {red} days recently.",
            "That’s how sessions were distributed."
        ]

    if topic == "BEST_WORST_DAY":
        best, worst = fact
        return [
            "Here’s a volatility snapshot.",
            f"Best day: {best} percent. Worst day: {worst} percent.",
            "That captures recent market swings."
        ]

def main():
    topic = choose_topic()
    data = fetch_nifty_data()
    fact = generate_fact(topic, data)
    script = generate_script(topic, fact)

    print({
        "topic": topic,
        "script": script
    })

if __name__ == "__main__":
    main()
