from mdrawbot.draw import Turtle
from mdrawbot.hilb import curve

t = Turtle()
try:
    t.up()
    t.goto(191, -200)
    t.down()
    t.follow(curve(7), 3)
finally:
    t.stop()
