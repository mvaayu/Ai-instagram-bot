import os
import yfinance as yf
from openai import OpenAI
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# -------------------------
# Fetch market data
# -------------------------
def fetch_market_data():
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")

    close = round(data["Close"].iloc[-1], 2)
    open_price = round(data["Open"].iloc[-1], 2)

    change = round(close - open_price, 2)
    percent = round((change / open_price) * 100, 2)

    return close, change, percent


# -------------------------
# Generate caption via AI
# -------------------------
def generate_caption(close, change, percent):

    prompt = f"""
    Create a short Instagram reel script.
    Neutral tone. No advice.
    Max 4 lines. Add emojis.

    NIFTY close {close}
    Change {change} ({percent}%)
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


# -------------------------
# Create reel video
# -------------------------
def create_video(text):

    W, H = 1080, 1920

    img = Image.new("RGB", (W, H), (15, 15, 20))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    wrapped = "\n".join(text.split(". "))

    draw.text((80, 700), wrapped, fill="white", font=font)

    img.save("frame.png")

    clip = ImageClip("frame.png").set_duration(12)

    clip.write_videofile("output.mp4", fps=24)


# -------------------------
# Main
# -------------------------
def main():
    print("🚀 Bot started")

    close, change, percent = fetch_market_data()

    caption = generate_caption(close, change, percent)

    print("\nCaption:\n", caption)

    create_video(caption)

    print("🎬 Video created: output.mp4")


if __name__ == "__main__":
    main()
