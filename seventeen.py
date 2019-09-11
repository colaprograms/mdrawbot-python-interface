import mdrawbot.draw as draw
import time
import math
import numpy as np

class Dummy:
    def start(self):
        pass

    def up(self):
        pass

    def serial_clear(self):
        pass

    def goto(self, x, y):
        print("gone to %f %f" % (x, y))
        pass

    def up(self):
        pass

    def down(self):
        pass

ACTUALLY_DRAW = True

if ACTUALLY_DRAW:
    d = draw.Drawer()
    d.set_up_down(120, 113)
    d.start()
    d.up()
else:
    d = Dummy()

XWIDTH = 360
YBOTTOM = -580
YTOP = -125
YCENTER = -352.5
SCALE = 200
WHEE = True

def xmap(x):
    x *= SCALE
    return x

def ymap(y):
    y *= SCALE # not a typo
    y += YCENTER
    return y

def goto(x, y):
    d.goto(xmap(x), ymap(y))

def drawline(x0, y0, x1, y1):
    d.up()
    goto(x0, y0)
    time.sleep(0.1)
    d.down()
    time.sleep(0.1)
    # should probably break into many smaller lines here
    goto(x1, y1)
    d.up()

def omega(x):
    return math.cos(2 * math.pi * x), math.sin(2 * math.pi * x)

def posn(n, j):
    return omega(j / n)

def drawchord(nn, a, b):
    x0, y0 = posn(nn, a)
    x1, y1 = posn(nn, b)
    drawline(x0, y0, x1, y1)

def drawcircle():
    goto(1, 0)
    time.sleep(2)
    d.down()
    time.sleep(2)
    for theta in np.linspace(0, 1, 1000):
        print("theta = %f" % theta)
        x, y = omega(theta)
        goto(x, y)

def draw(nn):
    for i in range(1, (nn-1)//2):
        fac = math.gcd(i, nn)
        for j in range(0, fac):
            x0, y0 = posn(nn, j)
            goto(x0, y0)
            time.sleep(2)
            cur = j
            for l in range(0, nn // fac):
                old = cur
                cur = (cur + i) % nn
                print("draw %d %d" % (old, cur))
                drawchord(nn, old, cur)

try:
    drawcircle()
    draw(17)
finally:
    print("Cancelling")
    d.serial_clear()
    d.up()
    d.goto(0, 0)
