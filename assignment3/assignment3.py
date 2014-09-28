#!/usr/bin/python2.7

from Tkinter import Tk
import guiInterface


def main():
    root = Tk()

    app = guiInterface.MainGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
