from Tkinter import *


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

            self.serverSelect = Radiobutton(
                self,
                text="Server",
                variable=self.mode,
                value=1,
                command=self.OnModeSelect
            )
            self.serverSelect.grid(column=1, columnspan=15, row=0, sticky='EW')

            self.clientSelect = Radiobutton(
                self,
                text="Client",
                variable=self.mode,
                value=2,
                command=self.OnModeSelect
            )
            self.clientSelect.grid(column=1, columnspan=15, row=1, sticky='EW')

            # IP Entry Widget
            self.ipLabel = Label(self, text="IP: ", anchor="w")
            self.ipLabel.grid(column=1, columnspan=2, row=2, sticky='EW')

            self.ipAddr = StringVar()
            self.ipEntry = Entry(self, textvariable=self.ipAddr)
            self.ipEntry.grid(column=3, columnspan=7, row=2, sticky='EW')

            # Port Entry Widget
            self.portLabel = Label(self, text="Port: ", anchor="w")
            self.portLabel.grid(column=10, columnspan=2, row=2, sticky='EW')

            self.port = StringVar()
            self.portEntry = Entry(self, textvariable=self.ipAddr)
            self.portEntry.grid(column=12, columnspan=4, row=2, sticky='EW')

            # Key Entry Widget
            self.KeyLabel = Label(self, text="Key: ", anchor="w")
            self.KeyLabel.grid(column=1, columnspan=2, row=3, sticky='EW')

            self.key = StringVar()
            self.keyEntry = Entry(self, textvariable=self.key)
            self.keyEntry.grid(column=3, columnspan=6, row=3, sticky='EW')

            # Connect Button
            self.connectButton = Button(
                self,
                text="Connect",
                command=self.OnConnectButtonPress
            )
            self.connectButton.grid(column=10, columnspan=6, row=3,
                                    sticky='EW')

            # Message Display
            self.messageLabel = Label(self, text="Messages: ", anchor="w")
            self.messageLabel.grid(column=1, columnspan=7, row=5, sticky='EW')

            self.messages = StringVar()
            self.messageDisplay = Label(
                self,
                height=9,
                anchor='w',
                justify='left',
                relief='sunken',
                textvariable=self.messages
            )
            self.messageDisplay.grid(column=1, columnspan=7, row=6, rowspan=10,
                                     sticky='EW')

            # Debug Display
            self.debugLabel = Label(self, text="Debug: ", anchor="w")
            self.debugLabel.grid(column=10, columnspan=5, row=5, sticky='EW')

            self.debug = StringVar()
            self.debugDisplay = Label(
                self,
                height=9,
                anchor='w',
                justify='left',
                relief='sunken',
                textvariable=self.debug
            )
            self.debugDisplay.grid(column=10, columnspan=5, row=6, rowspan=10,
                                   sticky='EW')

            # Continue Button
            self.continueButton = Button(self, text="Continue",
                                         command=self.OnContinueButtonPress)
            self.continueButton.grid(column=10, columnspan=6, row=16,
                                     sticky='EW')

            # Send Message Entry Widget
            self.sendMessageLabel = Label(self, text="Message To Send: ",
                                          anchor="w")
            self.sendMessageLabel.grid(column=1, columnspan=10, row=17,
                                       sticky='EW')

            self.sendMessage = StringVar()
            self.sendMessageEntry = Entry(self, textvariable=self.debug)
            self.sendMessageEntry.grid(column=1, columnspan=10, row=18,
                                       sticky='EW')

            # Send Button
            self.sendButton = Button(self, text="Send",
                                     command=self.OnSendButtonPress)
            self.sendButton.grid(column=12, columnspan=4, row=18, sticky='EW')

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

    def OnModeSelect(self):
            print("Selected " + str(self.mode.get()) + " mode")

    def OnConnectButtonPress(self):
            print("You pressed the connect button!")

    def OnContinueButtonPress(self):
            print("You pressed the continue button!")

    def OnSendButtonPress(self):
            print("You pressed the send button!")
