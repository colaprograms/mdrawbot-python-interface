import draw
import time
import numpy as np
from PIL import Image

class Dummy:
    def start(self):
        pass

    def up(self):
        pass

    def serial_clear(self):
        pass

    def goto(self, x, y):
        pass

    def down(self):
        pass

    def set_up_down(self, up, down):
        pass

if True:
    d = draw.Drawer()
    d.start()
    d.up()
else:
    d = Dummy()

XWIDTH = 360
YBOTTOM = -580
YTOP = -125
SCALE = 1.8
XOFFSET = 0

def xmap(x):
    x += XOFFSET
    x /= 4
    x *= SCALE
    return x

def ymap(y):
    y *= SCALE
    y = YTOP - y
    return y

def drawline(y, x0, x1):
    y = ymap(y)
    x0 = xmap(x0)
    x1 = xmap(x1)
    print("line %f %f %f" % (y, x0, x1))
    d.up()
    d.goto(x0, y)
    d.down()
    time.sleep(0.1)
    if x0 == x1:
        d.up()
    else:
        if x0 < x1:
            while x1 - x0 > 10:
                x0 += 10
                d.goto(x0, y)
        else:
            while x0 - x1 > 10:
                x0 -= 10
                d.goto(x0, y)
        d.goto(x1, y)
        d.up()

class Range:
    pass

def draw_hopper():
    global XOFFSET
    t = Image.open("hopper.png")
    w, h = t.size
    XOFFSET = -w / 2
    r = Range()
    r.on = False
    def eject():
        if r.on:
            drawline(r.h, r.start, r.end)
            r.on = False
    for i in range(h-1, -1, -1):
        if i & 1:
            rr = range(w-1, -1, -1)
        else:
            rr = range(w)
        for j in rr:
            if t.getpixel((j, i)) == 1:
                if not r.on:
                    r.start = j
                    r.end = j
                    r.h = i
                    r.on = True
                else:
                    r.end = j
            else:
                if r.on:
                    eject()
        eject()

try:
    d.set_up_down(120, 113)
    draw_hopper()
finally:
    print("Cancelling")
    d.serial_clear()
    d.up()
    d.goto(0, 0)
