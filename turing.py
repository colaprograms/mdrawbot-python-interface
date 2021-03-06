import mdrawbot.draw as draw
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

def xmap(x):
    x /= 4
    x -= 100
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

def draw_turing():
    t = Image.open("img/turing.png")
    w, h = t.size
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
    draw_turing()
finally:
    print("Cancelling")
    d.serial_clear()
    d.up()
    d.goto(0, 0)
