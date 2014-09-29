#!/usr/bin/python2.7

from Tkinter import Tk
from SWCZ import SWCZ


def main():
    root = Tk()

    app = SWCZ(root)
    root.mainloop()

if __name__ == "__main__":
    main()
