from MDNotes import MDNotes

if __name__ == '__main__':
    try:
        MDNotes().run()
    except KeyboardInterrupt:
        MDNotes().stop()