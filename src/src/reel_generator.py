import yfinance as yf
import matplotlib.pyplot as plt
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from datetime import datetime
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_data():
    nifty = yf.download("^NSEI", period="1mo", interval="1d")
    return nifty

def create_chart(data):
    plt.figure(figsize=(6,4))
    plt.plot(data.index, data["Close"])
    plt.title("NIFTY 50 – Last 1 Month")
    plt.tight_layout()
    path = f"{OUTPUT_DIR}/chart.png"
    plt.savefig(path)
    plt.close()
    return path

def create_reel(chart_path):
    img_clip = ImageClip(chart_path).set_duration(6)

    text = TextClip(
        "Market Snapshot\n(No Advice)",
        fontsize=50,
        color="white",
        size=img_clip.size,
        method="caption",
        align="center"
    ).set_duration(6)

    video = CompositeVideoClip([img_clip, text])
    video_path = f"{OUTPUT_DIR}/reel.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path

def generate_caption():
    today = datetime.now().strftime("%d %b %Y")
    return (
        f"Market recap | {today}\n\n"
        "Data-driven snapshot of NIFTY 50.\n"
        "Purely historical. No recommendations.\n\n"
        "#stockmarket #nifty50 #marketdata #investingfacts"
    )

def generate():
    data = fetch_data()
    chart = create_chart(data)
    video = create_reel(chart)
    caption = generate_caption()

    with open("output/caption.txt", "w") as f:
        f.write(caption)

    print("✅ Reel generated successfully")
