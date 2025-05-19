from rich import print
from luma.led_matrix.device import max7219
from luma.core.interface.serial import gpio_cs_spi
from luma.core.virtual import viewport, snapshot
from hotspot import clock, weather
import RPi.GPIO as GPIO
import signal
import sys
import time

# do BCM mode _before_ we touch any luma interface that uses GPIO
GPIO.setmode(GPIO.BCM)

NEW_CS_PIN = 23    # your chip-select on GPIO23
serial = gpio_cs_spi(
    port=0,
    device=0,
    gpio_CS=NEW_CS_PIN,    # <-- CS on pin 23
    bus_speed_hz=8_000_000  # one of the supported speeds
)

# shutdown flag
stop_requested = False
def _signal_handler(signum, frame):
    global stop_requested
    stop_requested = True
    sys.exit(0)

for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
    signal.signal(sig, _signal_handler)

width = 64
height = 24
device = max7219(
    serial,
    width=width,
    height=height,
    block_orientation=-90,
    contrast=1
)

def app():
    while True:
        virtual = viewport(device, width=device.width, height=device.height + 16)
        clk  = snapshot(64, 16, clock.render,   interval=1.0)
        wth  = snapshot(64, 16, weather.render, interval=10.0)
        virtual.add_hotspot(clk, (0, 0))
        virtual.add_hotspot(wth, (0, 15))
        virtual.set_position((0, 0))

if __name__ == "__main__":
    print('[yellow]Booting up...[/yellow]')
    time.sleep(4)
    device.contrast(20)

    try:
        app()
    except KeyboardInterrupt:
        device.clear()
