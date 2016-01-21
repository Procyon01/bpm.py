#!/usr/bin/python
import time

# Some VT100 control code magic
cursor_up = '\x1b[1A'
erase_line = '\x1b[2K'

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()



getch = _Getch()
beats = -1 
begin = 0 

print("BPM counter. Begin tapping for BPM...")

while True:
    key = ord(getch())
    if key == 27 or key == 3:   # Linux Escape or Ctrl+C
        exit(0)
    else:
        beats = beats + 1
	if beats == 0:
            begin = time.time()
            print('\n> First beat')
        else:
            interval = time.time() - begin
            interval_minutes = interval / 60
            bpm = int(beats / interval_minutes)
            print(cursor_up + erase_line + 'Average BPM > ' + str(bpm))
