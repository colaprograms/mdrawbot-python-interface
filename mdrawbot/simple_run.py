import mdrawbot.draw as draw

def simple_run(action, port="/dev/ttyUSB0"):
    d = draw.Drawer(port)
    d.start()
    action(d)
    d.serial_clear()
