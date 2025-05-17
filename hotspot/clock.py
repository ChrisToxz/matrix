from PIL import ImageFont
from datetime import datetime

previous_second = 0

def render(draw, width, height):
    global previous_second
    font = ImageFont.truetype("fonts/rabbit.ttf", 20)
    now = datetime.now()
    current_second = now.second

    draw.text((4, 2), now.strftime("%H:%M"), fill="white", font=font)
    print(current_second)
    draw.line(((2, 0), (current_second + 2, 0)), fill="white")

    if previous_second != current_second:
        draw.line(((0,0),(1,0)), fill="white")
        draw.line(((62,0),(63,0)), fill="white")
        previous_second = current_second