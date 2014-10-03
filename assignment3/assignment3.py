#!/usr/bin/python2.7
try:
    from Tkinter import Tk
except ImportError:
    from tkinter import Tk

from SWCZ import SWCZ
from SWCZPresenter import SWCZPresenter


def main():
    root = Tk()

    presenter = SWCZPresenter()
    view = SWCZ(presenter, root)
    presenter.bind(view)
    root.title("SWCZ")
    root.mainloop()

if __name__ == "__main__":
    main()
