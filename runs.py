import draw
import hilb

t = draw.Turtle()
try:
    t.up()
    t.goto(191, -200)
    t.down()
    t.follow(hilb.curve(7), 3)
finally:
    t.stop()
