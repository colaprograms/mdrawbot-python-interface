#!/usr/bin/python3

import serial
import time
import select
import sys, fcntl, os

class Term:
    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(port, 115200, timeout=0)
        time.sleep(1)
        self.recvbuf = b""
        self.sendbuf = ""
        flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        self.flags = flags
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def restore(self):
        flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        if flags != self.flags | os.O_NONBLOCK:
            raise Exception("flags are weird: %x != %x" % (
                flags,
                self.flags
            ))
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, self.flags)

    def clearnonblock(self):
        flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        flags &= ~os.O_NONBLOCK
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags)

    def loop(self):
        while True:
            self.go()

    def go(self):
        r, _, _ = select.select([self.serial, sys.stdin], [], [])
        for z in r:
            if z == self.serial:
                self.recvbuf += self.serial.read()
                self.recv()
            elif z == sys.stdin:
                self.sendbuf += sys.stdin.read()
                self.send()

    def recv(self):
        s = self.recvbuf.split(b"\n", 1)
        if len(s) > 1:
            print(s[0].decode("utf-8"))
            self.recvbuf = s[1]

    def send(self):
        s = self.sendbuf.split("\n", 1)
        if len(s) > 1:
            self.serial.write(s[0].encode("utf-8") + b"\n")
            self.sendbuf = s[1]

if __name__ == "__main__":
    term = Term()
    try:
        while True:
            term.go()
    finally:
        term.restore()
