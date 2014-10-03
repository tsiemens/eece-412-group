from SWCZ import SWCZ, ViewListener
import socket
import SWCZSocket

class SWCZPresenter(ViewListener, SWCZSocket.ResponseHandler,
                    SWCZSocket.MessageLogger):
   
    def bind(self, view):
        self.view = view
        self.socket = None
        self.swczsocket = None

    def add_message(self, sendername, text):
        self.view.add_message("{:s}:{:s}\n".format(sendername, text))

    def on_mode_select(self):
            print("Selected " + str(self.view.mode.get()) + " mode")

    def get_ip(self):
        ip = self.view.ip_addr.get()
        return ip if ip != None else ''

    def get_port(self):
        try:
            port = int(self.view.port.get())
            if port < 0 or port > 65535:
                raise Exception("Invalid port: " + str(port))
            return port
        except Exception as e:
            self.log(str(e))
            return None

    def on_connect_button_press(self):
        port = self.get_port()
        ip = self.get_ip()
        if port != None and ip != None:
            self.start_socket(ip, port)        

    def start_socket(self, ip, port):
        print("Creating socket with ip: %s, port: %d" % (ip, port))
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.view.is_mode_server():
            mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mysocket.bind((ip, port))
            mysocket.listen(1)
            conn, addr = mysocket.accept()
            self.log("Connected to %s!" % str(addr))
            self.socket = conn
        else:
            self.socket = mysocket
            self.socket.connect((ip, port))
            self.log("Connected!")

        self.swczsocket = SWCZSocket.SWCZSocket(self.socket, 2, 4, 6, "shared", True)
        self.swczsocket.set_logger(self)
        self.swczsocket.listen_async(self)

    def on_continue_button_press(self):
        print("You pressed the continue button!")

    def on_send_button_press(self):
        message = self.view.send_message.get()
        self.swczsocket.send(message)
        self.add_message("Me", message)

    def on_window_destroyed(self):
        if self.swczsocket:
           self.swczsocket.close() 

    def handle(self, message):
        """ Handle messages from the SWCZSocket """
        self.add_message("Bob", message)

    def log(self, message):
        self.view.add_debug_message(message + '\n')
  
