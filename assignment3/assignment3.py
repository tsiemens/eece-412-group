#!/usr/bin/python2.7
from Tkinter import *

def on_test_button_pressed():
    print("Button pressed")

def main():
    print("Hello World!") 
    root = Tk()
    # a test button
    test_button = Button(root, text='Test',
                         command=on_test_button_pressed)
    test_button.grid(row=0, column=0)
    test_button.pack(pady=20, padx = 20)
   
    root.mainloop()

if __name__ == "__main__":
    main()
