try:
	from Tkinter import *
except ImportError:
	from tkinter import *
	
class SWCZ(Frame):
    def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.parent = parent
            self.initialize()

    def initialize(self):
            self.grid()

            # Client/Server Radio Buttons
            self.mode = IntVar()
            self.mode.set(2)  # initialize to client

            self.server_select = Radiobutton(
                self,
                text="Server",
                variable=self.mode,
                value=1,
                command=self.on_mode_select
            )
            self.server_select.grid(column=1, columnspan=15, row=0, sticky='EW')

            self.client_select = Radiobutton(
                self,
                text="Client",
                variable=self.mode,
                value=2,
                command=self.on_mode_select
            )
            self.client_select.grid(column=1, columnspan=15, row=1, sticky='EW')

            # IP Entry Widget
            self.ip_label = Label(self, text="IP: ", anchor="w")
            self.ip_label.grid(column=1, columnspan=2, row=2, sticky='EW')

            self.ip_addr = StringVar()
            self.ip_entry = Entry(self, textvariable=self.ip_addr)
            self.ip_entry.grid(column=3, columnspan=7, row=2, sticky='EW')

            # Port Entry Widget
            self.port_label = Label(self, text="Port: ", anchor="w")
            self.port_label.grid(column=10, columnspan=2, row=2, sticky='EW')

            self.port = StringVar()
            self.port_entry = Entry(self, textvariable=self.port)
            self.port_entry.grid(column=12, columnspan=4, row=2, sticky='EW')

            # Key Entry Widget
            self.Key_label = Label(self, text="Key: ", anchor="w")
            self.Key_label.grid(column=1, columnspan=2, row=3, sticky='EW')

            self.key = StringVar()
            self.key_entry = Entry(self, textvariable=self.key)
            self.key_entry.grid(column=3, columnspan=6, row=3, sticky='EW')

            # Connect Button
            self.connect_button = Button(
                self,
                text="Connect",
                command=self.on_connect_button_press
            )
            self.connect_button.grid(column=10, columnspan=6, row=3,
                                    sticky='EW')

            # Message Display
            self.message_label = Label(self, text="Messages: ", anchor="w")
            self.message_label.grid(column=1, columnspan=7, row=5, sticky='EW')

            self.messages = StringVar()
            self.message_display = Label(
                self,
                height=9,
                anchor='w',
                justify='left',
                relief='sunken',
                textvariable=self.messages
            )
            self.message_display.grid(column=1, columnspan=7, row=6, rowspan=10,
                                     sticky='EW')

            # Debug Display
            self.debug_label = Label(self, text="Debug: ", anchor="w")
            self.debug_label.grid(column=10, columnspan=5, row=5, sticky='EW')

            self.debug = StringVar()
            self.debug_display = Label(
                self,
                height=9,
                anchor='w',
                justify='left',
                relief='sunken',
                textvariable=self.debug
            )
            self.debug_display.grid(column=10, columnspan=5, row=6, rowspan=10,
                                   sticky='EW')

            # Continue Button
            self.continue_button = Button(self, text="Continue",
                                         command=self.on_continue_button_press)
            self.continue_button.grid(column=10, columnspan=6, row=16,
                                     sticky='EW')

            # Send Message Entry Widget
            self.send_message_label = Label(self, text="Message To Send: ",
                                          anchor="w")
            self.send_message_label.grid(column=1, columnspan=10, row=17,
                                       sticky='EW')

            self.send_message = StringVar()
            self.send_message_entry = Entry(self, textvariable=self.send_message)
            self.send_message_entry.grid(column=1, columnspan=10, row=18,
                                       sticky='EW')

            # Send Button
            self.send_button = Button(self, text="Send",
                                     command=self.on_send_button_press)
            self.send_button.grid(column=12, columnspan=4, row=18, sticky='EW')

            # General Configuration
            self.grid_columnconfigure(0, weight=1)
            for i in range(1, 15):
                    self.grid_columnconfigure(i, weight=10, minsize=5)
            self.grid_columnconfigure(16, weight=1)

            for i in range(0, 17):
                    self.grid_rowconfigure(i, weight=10, minsize=5)

            self.parent.resizable(True, False)
            self.update()
            #self.geometry(self.geometry())

    def on_mode_select(self):
            print("Selected " + str(self.mode.get()) + " mode")

    def on_connect_button_press(self):
            print("You pressed the connect button!")

    def on_continue_button_press(self):
            print("You pressed the continue button!")

    def on_send_button_press(self):
            print("You pressed the send button!")