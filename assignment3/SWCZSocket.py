import socket
from threading import Thread

EOF = '\x04'
DER = '\\'

class ResponseHandler:
    def handle(self, message):
        pass

def count_derefs_before(string, index):
    deref_count = 0
    for i in range(index - 1, -1, -1):
        if string[i] == DER:
            deref_count += 1
        else:
            return deref_count, False
    return deref_count, True


def is_char_derefed(buff, char_index, msg):
    deref_count, is_to_first = count_derefs_before(buff, char_index)
    if not is_to_first:
        return deref_count % 2 != 0
        
    deref_count += count_derefs_before(msg, len(msg))[0]
    return deref_count % 2 != 0

def get_eof_index(buff, msg):
    for i in range(0, len(buff)):
        if buff[i] == EOF and not is_char_derefed(buff, i, msg):
            return i
    return -1

class ResponseThread(Thread):
    def __init__(self, secure_socket):
        super(ResponseThread, self).__init__()
        self.swcz = secure_socket

    def run(self):
        message = ''
        while True:
            try:
                buff = self.swcz.socket.recv(1024)
            except:
                return
            eof_index = get_eof_index(buff, message)
            if eof_index == -1:
                message += buff
            else:
                message += buff[:eof_index]
                self.swcz.handle(message)
                message = buff[eof_index + 1:]

class SWCZSocket:
    """ Creates new secure socket layout wrapper around sock,
        a socket.socket
        The socket uses the value g, p, secret_int for encryption,
        and shared_key for authorization """
    
    def __init__(self, sock, g, p, secret_int, shared_key, is_server):
        self.socket = sock
        self.g = g
        self.p = p
        self.secret = secret_int
        self.shared_key = shared_key
        self.gen_key = None

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        pass # TODO

    def listen_async(self, handler):
        self.handler = handler
        self.response_thread = ResponseThread(self)
        self.response_thread.start()

    def send(self, message):
        socket.send(message) # TODO do encryption

    def handle(self, message):
        if self.handler is not None:
            self.handler.handle(message)

    def close(self):
        self.socket.close()

