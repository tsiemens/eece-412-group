#!/usr/bin/python2.7
try:
    from Tkinter import Tk
except ImportError:
    from tkinter import Tk

from SWCZ import SWCZ


def main():
    root = Tk()

    SWCZ(root)
    root.title("SWCZ")
    root.mainloop()

if __name__ == "__main__":
    main()
