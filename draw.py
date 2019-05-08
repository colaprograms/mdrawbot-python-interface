import serial
import re
import time

regex = r'^M10 MSPIDER (\d+) (\d+) 0.00 0.00 A([01]) B([01]) H0 S90 U(\d+) D0$'

""" Commands:

    M10
        M10 MSPIDER 940 1530 0.00 0.000 A0 b0 H0 S90 U113 D0
        OK

    H: hang distance
    W: width between two strings
    A: left motor is clockwise (0) or counterclockwise (1)
    B: right motor is clockwise (0) or counterclockwise (1)
    S: idk lol

    M5 A1 B1 H940 W1530 S90
        OK

    100: servo angle

    M1 113
        OK

    G1 X-0.00 Y0.00
        OK
"""

class UnexpectedResponse (Exception):
    pass

class Drawer:
    DELAY = 2

    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(port, 115200)
        time.sleep(2.0)
        self.started = False
        self.waiting = False
        self.up_angle = 113
        self.down_angle = 107

    def set_up_down(self, up, down):
        self.validate_angle(up)
        self.validate_angle(down)
        self.up_angle = up
        self.down_angle = down

    def validate_angle(self, angle):
        if 90 <= angle <= 130:
            return
        raise Exception("angle is not good")

    def start(self):
        now = time.time()
        if not self.started:
            self.send("M10")
            r1 = self.recv()
            self.validate(r1)
            r2 = self.recv("OK")
            self.started = True

    def validate(self, msg):
        m = re.match(r'^M10 MSPIDER (\d+) (\d+) 0.00 0.00 A([01]) B([01]) H0 S90 U(\d+) D0$', msg)
        if m is not None:
            h, w, a, b, u = m.group(1, 2, 3, 4, 5)
            if h == "360" and w == "1530" and a == "1" and b == "1":
                u = int(u)
                print("pen angle = %d" % u)
                return
        print("got invalid response: %s" % msg)
        raise Exception("invalid response")

    def goto(self, x, y):
        self.send("G1 X%.2f Y%.2f" % (-x, y))
        self.recv("OK")

    def angle(self, th):
        self.send("M1 %d" % th)
        self.recv("OK")

    def send(self, msg):
        print(msg)
        self.serial.write(msg.encode("utf-8") + b"\n")

    def recv(self, expecting=None):
        self.waiting = True
        msg = self.serial.readline().decode("utf-8").strip()
        self.waiting = False
        print(" " * 8 + msg)
        if expecting is not None:
            if msg != expecting:
                print("unexpected response: %s is not %s" % (msg, expecting))
                raise UnexpectedResponse()
        return msg

    def serial_clear(self):
        if self.waiting:
            self.serial.readline()
        self.waiting = False

    def up(self):
        self.angle(self.up_angle)

    def down(self):
        self.angle(self.down_angle)

    def fileno(self):
        return self.serial.fileno()

class Turtle:
    def __init__(self):
        self.drawer = Drawer()
        self.bounds = (-200, -200, 200, 200)
        self.dir = (0, 1)
        self.pos = (0, 0)

        time.sleep(2)
        self.drawer.start()

    def stop(self):
        self.up()
        self.goto(0, 0)

    def up(self):
        self.drawer.angle(130)

    def down(self):
        self.drawer.angle(100)

    def left(self):
        x, y = self.dir
        self.dir = (-y, x)

    def right(self):
        x, y = self.dir
        self.dir = (y, -x)

    def ahead(self, dist):
        x, y = self.dir
        self.move_relative(x * dist, y * dist)

    def move_relative(self, x, y):
        X, Y = self.pos
        X += x
        Y += y
        self.goto(X, Y)

    def goto(self, x, y):
        if self.in_bounds(x, y):
            self.drawer.goto(x, y)
            self.pos = x, y

    def in_bounds(self, x, y):
        x0, y0, x1, y1 = self.bounds
        return x0 <= x <= x1 and y0 <= y <= y1

    def follow(self, s, dist, wait=0.4):
        for c in s:
            if c == "-":
                self.left()
            elif c == "+":
                self.right()
            elif c == "F":
                self.ahead(dist)
                time.sleep(wait)
        self.stop()
