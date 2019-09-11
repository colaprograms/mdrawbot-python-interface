import mdrawbot.draw as draw
import time
import numpy as np

d = draw.Drawer()
d.start()
d.up()

XWIDTH = 360
YBOTTOM = -580
YTOP = -125
RESOLUTION = 10

def run(SMALL):
    xwidth = XWIDTH - SMALL
    ybottom = YBOTTOM + SMALL
    ytop = YTOP - SMALL

    d.goto(-xwidth, ybottom)
    d.down()
    time.sleep(2)
    for i in np.linspace(-xwidth, xwidth, RESOLUTION):
        d.goto(i, ybottom)
    for i in np.linspace(ybottom, ytop, RESOLUTION):
        d.goto(xwidth, i)
    for i in np.linspace(xwidth, -xwidth, RESOLUTION):
        d.goto(i, ytop)
    for i in np.linspace(ytop, ybottom, RESOLUTION):
        d.goto(-xwidth, i)
    d.up()
    d.goto(0, 0)

try:
    for i in range(0, 120, 10):
        run(i)
finally:
    print("Cancelling")
    d.serial_clear()
    d.up()
    d.goto(0, 0)
