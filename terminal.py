import mdrawbot.terminal

if __name__ == "__main__":
    term = mdrawbot.terminal.Term()
    try:
        while True:
            term.go()
    finally:
        term.restore()
