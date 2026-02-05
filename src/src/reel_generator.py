from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips

WIDTH, HEIGHT = 1080, 1920
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
DURATION_PER_SLIDE = 2

lines = [
    "NIFTY 50 – Market Recap",
    "Previous Close: 21,982",
    "+0.63% Today",
    "Volatility remained moderate"
]

clips = []

for line in lines:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Default font (safe on GitHub Actions)
    font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), line, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (WIDTH - text_width) / 2
    y = (HEIGHT - text_height) / 2

    draw.text((x, y), line, fill=TEXT_COLOR, font=font)

    img_path = f"frame_{len(clips)}.png"
    img.save(img_path)

    clip = ImageClip(img_path).set_duration(DURATION_PER_SLIDE)
    clips.append(clip)

final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile("reel.mp4", fps=24)
