from AsyncMsgSocket import AsyncMsgSocket


class SWCZSocket(object):
    """ Creates new secure socket layout wrapper around sock,
        a socket.socket
        The socket uses the value g, p, secret_int for encryption,
        and shared_key for authorization """

    def __init__(self, frame, sock, g, p, secret_int, shared_key, is_server):
        self.frame = frame
        self.g = g
        self.p = p
        self.secret = secret_int
        self.shared_key = shared_key
        self.gen_key = None
        self.logger = None

        self.socket = AsyncMsgSocket(frame, sock)

        self.socket.listen_async(self)

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        pass  # TODO

    def send(self, msg):
        # TODO: encrypt
        self.socket.send(msg)

    def advance_queue(self):
        self.socket.advance_queue()

    def handle_response(self, msg):
        self.frame.add_message("Them", msg)

    def close(self):
        self.socket.close()
