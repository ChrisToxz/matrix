import time
import requests
from PIL import ImageFont
from rich import print
from rich.pretty import pprint

last_update = 0
weather_data = None

# ——— module-scope state ———
current_msg      = 0
msg_switched     = 0.0        # when we started this message
end_reached_time = None       # “freeze” point when we've scrolled fully in
scroll_speed     = 25.0       # px/sec
switch_delay     = 3.0        # static lines: secs to hold
hold_delay       = 1.0        # marquee lines: extra hold at end

def rate_limit(seconds: float):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global last_update
            now = time.time()
            if now - last_update >= seconds:
                last_update = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(60)
def update_weather():
    global weather_data
    r = requests.get(
        'https://weerlive.nl/api/json-data-10min.php',
        params={'key': 'b9a069cd2b', 'locatie': 'Almere'}
    )

    try:
        payload = r.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"[red]⚠️ JSON decode failed: {e}[/red]")
        print("[yellow]Raw response was:[/yellow]")
        pprint(r.text)
        return  # bail out, keep the old weather_data

    live = payload.get('liveweer')
    if not live or not isinstance(live, list):
        print("[red]⚠️ Unexpected payload structure:[/red]")
        pprint(payload)
        return  # again, don’t overwrite weather_data

    # finally, safe to update
    weather_data = live[0]
    print(f"[blue]Weather updated: {weather_data['temp']}°C[/blue]")


def render(draw, width, height):
    global current_msg, msg_switched, end_reached_time

    update_weather()
    msgs = [
        f"Nu: {weather_data['temp']}°C",
        f"{weather_data['samenv']}",
        f"Min: {weather_data['d0tmin']}°C",
        f"Max: {weather_data['d0tmax']}°C",
        f"Regen: {weather_data['d0neerslag']}%",
        f"Morgen: {weather_data['d1tmin']}/{weather_data['d1tmax']}°C - {weather_data['verw']}",
    ]
    text = msgs[current_msg]

    font = ImageFont.truetype("fonts/slkscr.ttf", 8)
    text_width = draw.textlength(text)
    now = time.time()

    # — static short text? —
    if text_width <= width:
        end_reached_time = None
        x = 0
        if now - msg_switched >= switch_delay:
            current_msg = (current_msg + 1) % len(msgs)
            msg_switched = now

    # — marquee long text —
    else:
        raw_offset = (now - msg_switched) * scroll_speed

        if raw_offset < text_width and end_reached_time is None:
            # still scrolling in
            x = width - raw_offset

        else:
            # we've reached the “end” (right edge)
            if end_reached_time is None:
                end_reached_time = now   # freeze starting now
            x = width - text_width      # lock at final position

            # after hold_delay, advance
            if now - end_reached_time >= hold_delay:
                current_msg = (current_msg + 1) % len(msgs)
                msg_switched = now
                end_reached_time = None

    draw.text((int(x), 0), text, fill="white", font=font)
