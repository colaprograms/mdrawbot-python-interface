from mdrawbot.server import DrawbotServer

if __name__ == "__main__":
    s = DrawbotServer()
    try:
        s.run()
    finally:
        s.stop()
