#!/usr/bin/python3

import socket
import threading
import select
import draw

def shutdown(sck):
    sck.shutdown(socket.SHUT_RDWR)

WIDTH = 360
HEIGHT = 227
YOFFSET = -352
MINPEN = 90
MAXPEN = 130

class _shared:
    def __init__(self):
        self.lock = threading.Lock()
        self.stop = False
        self.stopped = threading.Event()
        self.stopped.set()
        self.drawer = draw.Drawer()
        self.drawer.start()

class DrawbotThread:
    def __init__(self, sock, shar):
        self.sock = sock
        self.inet_buf = ""
        self.draw_buf = ""
        self.shar = shar
    def go(self):
        print("started thread")
        with self.shar.lock:
            if not self.shar.stopped.is_set():
                success = False
            else:
                self.shar.stopped.clear()
                success = True
        if success:
            self.actually_go()
        else:
            self.write("ERROR Some other jerk is already connected")
            shutdown(self.sock)
    def actually_go(self):
        self.write("OK You have control of the DrawBot")
        try:
            while True:
                r, _, _ = select.select([self.sock], [], [], 1)
                if self.shar.stop:
                    break
                if len(r) > 0:
                    re = self.sock.recv(4096)
                    if len(re) == 0:
                        break
                    self.inet_buf += re.decode("utf-8")
                    s = self.inet_buf.split("\n", 1)
                    if len(s) > 1:
                        self.inet_buf = s[1]
                        self.cmd(s[0])
        finally:
            print("stopped")
            shutdown(self.sock)
            self.shar.drawer.serial_clear()
            self.shar.drawer.up()
            self.shar.drawer.goto(0, 0)
            self.shar.stopped.set()
    def cmd(self, wh):
        try:
            z, *a = wh.split(" ")
            error = None
            z = z.upper()
            if z == "GOTO":
                error = self.goto(a)
            elif z == "UP":
                error = self.up(a)
            elif z == "DOWN":
                error = self.down(a)
            elif z == "SET_UP_DOWN":
                error = self.set_up_down(a)
            else:
                error = "idk what command that is lol"
        except Exception as e:
            print(str(e))
            error = "code is bad, blame hannah"
        if error is None:
            self.write("OK")
        else:
            self.write("ERROR " + error)
    def goto(self, a):
        error = None
        if len(a) != 2:
            error = "goto needs two arguments, x and y"
        if error is None:
            try:
                x = float(a[0])
            except:
                error = "x is not a number"
        if error is None:
            try:
                y = float(a[1])
            except:
                error = "y is not a number"
        if error is None:
            if x < -WIDTH:
                error = "x is too small (%d to %d)" % (-WIDTH, WIDTH)
            elif x > WIDTH:
                error = "x is too large (%d to %d)" % (-WIDTH, WIDTH)
            elif y < -HEIGHT:
                error = "y is too small (%d to %d)" % (-HEIGHT, HEIGHT)
            elif y > HEIGHT:
                error = "y is too large (%d to %d)" % (-HEIGHT, HEIGHT)
        if error is None:
            try:
                self.shar.drawer.goto(x, y + YOFFSET)
            except draw.UnexpectedResponse:
                error = "unexpected response"
        return error
    def up(self, ar):
        error = None
        if len(ar) != 0:
            error = "up needs no parameters"
        if error is None:
            try:
                self.shar.drawer.up()
            except draw.UnexpectedResponse:
                error = "unexpected response"
        return error
    def down(self, a):
        error = None
        if len(a) != 0:
            error = "down needs no parameters"
        if error is None:
            try:
                self.shar.drawer.down()
            except draw.UnexpectedResponse:
                error = "unexpected response"
        return error
    def set_up_down(self, a):
        error = None
        if len(a) != 2:
            error = "set_up_down needs two parameters, up and down"
        if error is None:
            try:
                up = int(a[0])
            except:
                error = "up is not an integer"
        if error is None:
            try:
                down = int(a[1])
            except:
                error = "down is not an integer"
        if error is None:
            def complain(name, way):
                return "%s is too %s (%d-%d)" % (name,way,MINPEN,MAXPEN)
            if up < MINPEN:
                error = complain("up", "small")
            elif up > MAXPEN:
                error = complain("up", "large")
            elif down < MINPEN:
                error = complain("down", "small")
            elif down > MAXPEN:
                error = complain("down", "large")
        if error is None:
            try:
                self.shar.drawer.set_up_down(up, down)
            except draw.UnexpectedResponse:
                error = "unexpected response"
        return error
    def write(self, tx):
        self.sock.send(tx.encode("utf-8") + b"\n")

class DrawbotServer:
    DRAWBOT_PORT = 34442
    def __init__(self):
        self.shared = _shared()
        host = "0.0.0.0"
        port = DrawbotServer.DRAWBOT_PORT
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def run(self):
        self.sock.listen(5)
        while True:
            print("waiting for sockets")
            c, a = self.sock.accept()
            c.settimeout(0)
            thread = DrawbotThread(c, self.shared)
            threading.Thread(target = thread.go).start()

    def stop(self):
        with self.shared.lock:
            self.shared.stop = True
        self.shared.stopped.wait()
        shutdown(self.sock)

if __name__ == "__main__":
    s = DrawbotServer()
    try:
        s.run()
    finally:
        s.stop()
