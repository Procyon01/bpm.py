#!/usr/bin/python
import time

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
beats = 0
begin = 0
try:
    while True:
        key = ord(getch())
        if key == 9:
            exit(0)
        else:
            beats = beats + 1
            if beats == 1:
                begin = time.time()
                continue
            else:
                interval = time.time() - begin
                interval_minutes = interval / 60
                bpm = beats / interval_minutes
                print(bpm)
except KeyboardInterrupt:
    exit(0)
