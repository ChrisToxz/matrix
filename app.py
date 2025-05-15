from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, snapshot
from hotspot import clock

width = 64
height = 24
serial = spi(port=0, device=0, gpio=noop(), baudrate=10000000000000)
device = max7219(serial, width=width, height=height, block_orientation=-90, contrast=1)   

def app():
    while True:
        virtual = viewport(device, width=device.width, height=device.height+16)
        clk = snapshot(64, 16, clock.render, interval=1.0)
        

        virtual.add_hotspot(clk, (0, 0))

        virtual.set_position((0, 0))

if __name__ == "__main__":

    device.clear()
    device.contrast(20)
    
    try:
        app()
    except KeyboardInterrupt:
        pass
    