from moviepy.editor import TextClip, CompositeVideoClip

WIDTH = 1080
HEIGHT = 1920
DURATION = 8

lines = [
    "NIFTY 50 – Market Recap",
    "Previous Close: 21,982",
    "+0.63% Today",
    "Volatility remained moderate"
]

clips = []
start = 0

for line in lines:
    txt = TextClip(
        line,
        fontsize=70,
        color="white",
        size=(WIDTH - 100, None),
        method="caption",
        align="center"
    ).set_position("center").set_start(start).set_duration(2)

    clips.append(txt)
    start += 2

background = TextClip(
    "",
    size=(WIDTH, HEIGHT),
    bg_color="black",
    duration=DURATION
)

video = CompositeVideoClip([background] + clips)
video.write_videofile("reel.mp4", fps=24)
