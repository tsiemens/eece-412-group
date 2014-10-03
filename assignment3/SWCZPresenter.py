import socket

import SWCZSocket
from SWCZ import ViewListener


class SWCZPresenter(ViewListener, SWCZSocket.ResponseHandler,
                    SWCZSocket.MessageLogger):
    def bind(self, view):
        self.view = view
        self.socket = None
        self.swczsocket = None

    def add_message(self, sendername, text):
        self.view.add_message("{}:{}\n".format(sendername, text))

    def on_mode_select(self):
            print("Selected mode {}".format(str(self.view.mode.get())))

    def get_ip(self):
        ip = self.view.ip_addr.get()
        return ip if ip is not None else ''

    def get_port(self):
        try:
            port = int(self.view.port.get())
            if port < 0 or port > 65535:
                # using str(port) here because it could be None
                raise Exception("Invalid port: {}".format(str(port)))
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
        print("Creating socket with ip: {}, port: {:d}".format(ip, port))
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.view.is_mode_server():
            mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mysocket.bind((ip, port))
            mysocket.listen(1)
            conn, addr = mysocket.accept()
            self.log("Connected to {}!".format(addr))
            self.socket = conn
        else:
            self.socket = mysocket
            self.socket.connect((ip, port))
            self.log("Connected!")

        self.swczsocket = SWCZSocket.SWCZSocket(self.socket, 2, 4, 6, "shared",
                                                True)
        self.swczsocket.set_logger(self)
        self.swczsocket.queue_mode = True
        self.swczsocket.listen_async(self)

    def on_continue_button_press(self):
        self.swczsocket.advance_queue()

    def on_send_button_press(self):
        message = self.view.send_message.get()
        self.swczsocket.send(message)
        self.add_message("Me", message)

    def on_window_destroyed(self):
        if self.swczsocket:
            self.swczsocket.close()

    def handle_response(self, message):
        """ Handle messages from the SWCZSocket """
        self.add_message("Them", message)

    def log(self, message):
        self.view.add_debug_message(message + '\n')
