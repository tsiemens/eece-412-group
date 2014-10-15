import socket
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from SWCZSocket import SWCZSocket

RADIO_SERVER = 1
RADIO_CLIENT = 2


class SWCZ(Frame):
    def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.parent = parent
            self.swczsocket = None
            self.log_queue = Queue()
            self.initialize()
            self.parent.after(200, self.process_log_queue)

    def initialize(self):
            self.grid(sticky=NSEW)

            # Client/Server Radio Buttons
            self.mode = IntVar()
            self.mode.set(2)  # initialize to client

            self.server_select = Radiobutton(
                self,
                text="Server",
                variable=self.mode,
                value=RADIO_SERVER,
                command=self.on_mode_select
            )
            self.server_select.grid(column=1, columnspan=15, row=0,
                                    sticky='EW')

            self.client_select = Radiobutton(
                self,
                text="Client",
                variable=self.mode,
                value=RADIO_CLIENT,
                command=self.on_mode_select
            )
            self.client_select.grid(column=1, columnspan=15, row=1,
                                    sticky='EW')

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
            self.port.set("8080") # our default port
            self.port_entry = Entry(self, textvariable=self.port)
            self.port_entry.grid(column=12, columnspan=4, row=2, sticky='EW')

            # Key Entry Widget
            self.Key_label = Label(self, text="Key: ", anchor="w")
            self.Key_label.grid(column=1, columnspan=2, row=3, sticky='EW')

            self.key = StringVar()
            self.key.set("defaultkey")
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

            self.message_display = Text(
                self,
                height=9,
                relief='sunken'
            )
            self.message_display.grid(column=1, columnspan=7, row=6,
                                      rowspan=10, sticky='EW')

            # Debug Display
            self.debug_label = Label(self, text="Debug: ", anchor="w")
            self.debug_label.grid(column=10, columnspan=5, row=5, sticky='EW')

            self.debug_display = Text(
                self,
                height=9,
                relief='sunken',
            )
            self.debug_display.grid(column=10, columnspan=5, row=6, rowspan=10,
                                    sticky='EW')

            # Continue Button
            self.continue_button = Button(
                self,
                text="Continue",
                command=self.on_continue_button_press,
                state=DISABLED
            )
            self.continue_button.grid(column=10, columnspan=6, row=16,
                                      sticky='EW')

            # Send Message Entry Widget
            self.send_message_label = Label(self, text="Message To Send: ",
                                            anchor="w")
            self.send_message_label.grid(column=1, columnspan=10, row=17,
                                         sticky='EW')

            self.send_message = StringVar()
            self.send_message_entry = Entry(self,
                                            textvariable=self.send_message)
            self.send_message_entry.grid(column=1, columnspan=10, row=18,
                                         sticky='EW')

            # Send Button
            self.send_button = Button(
                self,
                text="Send",
                command=self.on_send_button_press
            )
            self.send_button.grid(column=12, columnspan=4, row=18, sticky='EW')

            # General Configuration
            self.grid_columnconfigure(0, weight=1)
            for i in range(1, 15):
                    self.grid_columnconfigure(i, weight=1, minsize=5)
            self.grid_columnconfigure(16, weight=1)

            for i in range(0, 17):
                    self.grid_rowconfigure(i, weight=1, minsize=5)

            self.parent.resizable(True, False)
            self.parent.grid_columnconfigure(0, weight=1)
            self.parent.grid_rowconfigure(0, weight=1)
            self.update()

            self.parent.protocol("WM_DELETE_WINDOW", self._delete_window)

    def _delete_window(self):
        print("delete")
        try:
            if self.swczsocket:
                self.swczsocket.close()
            self.parent.destroy()
        except Exception as e:
            print(str(e))

    def is_mode_server(self):
        return self.mode.get() == RADIO_SERVER

    def add_message(self, sendername, text):
        self.add_lines_to_text(
            self.message_display,
            "{}:{}\n".format(sendername, text)
        )

    def add_debug_message(self, message):
        self.add_lines_to_text(self.debug_display, message)

    @staticmethod
    def add_lines_to_text(tktext, message):
        tktext.insert(END, message)
        tktext.see(END)

    def on_mode_select(self):
            print("Selected mode {}".format(self.mode.get()))

    def get_ip(self):
        ip = self.ip_addr.get()
        return ip if ip is not None else ''

    def get_port(self):
        try:
            port = int(self.port.get())
            if port < 0 or port > 65535:
                raise Exception("Invalid port: {}".format(port))
            return port
        except Exception as e:
            self.log(str(e))
            return None

    def on_connect_button_press(self):
        port = self.get_port()
        ip = self.get_ip()
        if port is not None and ip is not None:
            self.start_socket(ip, port)

    def start_socket(self, ip, port):
        print("Creating socket with ip: {}, port: {}".format(ip, port))
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.is_mode_server():
            mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mysocket.bind((ip, port))
            mysocket.listen(1)
            conn, addr = mysocket.accept()
            self.log("Connected to {}!".format(addr))
            self.socket = conn
        else:
            self.socket = mysocket
            self.socket.settimeout(10)
            connected = False
            try:
                self.socket.connect((ip, port))
                connected = True
                self.log("Connected!")
            except ConnectionRefusedError:
                print("Connection Refused")
            except TimeoutError:
                print("Connection Timeout")
            except Exception as e:
                print(str(e))
            finally:
                if not connected:
                    return

        self.swczsocket = SWCZSocket(
            self,
            self.socket,
            self.key.get(),
            self.is_mode_server(),
        )

    def on_continue_button_press(self):
        self.swczsocket.socket.advance_queue()

    def on_send_button_press(self):
        message = self.send_message.get()
        self.swczsocket.send(message)

    def set_continue_button_enabled(self, enabled):
        self.continue_button.config(state=NORMAL if enabled else DISABLED)

    def log(self, message):
        self.add_debug_message(message + '\n')

    def append_log_queue(self, msg):
        self.log_queue.put(msg)

    def process_log_queue(self):
        if not self.log_queue.empty():
            msg = self.log_queue.get()
            self.log(msg)

        self.parent.after(200, self.process_log_queue)
