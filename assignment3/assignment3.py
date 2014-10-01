#!/usr/bin/python2.7
try:
	from Tkinter import Tk
except ImportError:
	from tkinter import Tk
	
from SWCZ import SWCZ


def main():
    root = Tk()

    app = SWCZ(root)
    root.mainloop()

if __name__ == "__main__":
	main()
