#!/usr/bin/python3

from mdrawbot.simple_run import simple_run
import sys

actions = {
    "left": lambda drawer: drawer.goto(-100, 0),
    "right": lambda drawer: drawer.goto(100, 0),
    "up": lambda drawer: drawer.goto(0, 200),
    "down": lambda drawer: drawer.goto(0, -200)
}

def print_usage():
    print("python move.py [left|right] <distance>")
    print("    moves left or right by <distance>")
    print("    <distance> must be between -200 and +200")
    print()
    print("python move.py [up|down]")
    print("    moves up or down 200 units")
    sys.exit(1)

if __name__ == "__main__":
    parsed = None
    _, action, param, *_ = sys.argv + [None, None]
    if len(sys.argv) == 2:
      if action == "up":
        parsed = (0, 200)
      elif action == "down":
        parsed = (0, -200)
    elif len(sys.argv) == 3:
      if action == "left" or action == "right":
        try:
            param = float(param)
        except ValueError:
            print("parameter could not be parsed as a float")
        if action == "left":
            param = -param
        if param < -200:
          print("parameter cannot be < -200")
        elif param > 200:
          print("parameter cannot be > 200")
        else:
          parsed = (param, 0)
    if parsed is not None:
        simple_run(lambda drawer: drawer.goto(*parsed))
    else:
        print_usage()
