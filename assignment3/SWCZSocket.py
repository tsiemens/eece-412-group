from math import factorial
from modgrammar import ParseError
from Crypto.Random.random import randint

from AsyncMsgSocket import AsyncMsgSocket
from SWCZParser import InitMsgHeader, AuthMsgHeader


class SWCZSocket(object):
    """ Creates new secure socket layout wrapper around sock,
        a socket.socket
        The socket uses the value g, p, secret_int for encryption,
        and shared_key for authorization """

    def __init__(self, frame, sock, shared_key, is_server):
        self.frame = frame
        self.g = 2
        self.p = (factorial(300) - 1) * 2 + 1
        self.shared_key = shared_key
        self.is_server = is_server
        self.secret_int = randint(0, pow(2, 256))
        self.session_key = None
        self.state = "INIT"

        self.socket = AsyncMsgSocket(frame, sock)
        self.socket.listen_async(self)

        if not is_server:
            self.do_handshake()

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        A = pow(self.g, self.secret_int, self.p)
        self.send("SWCZ/1.0; INIT:  S={}".format(A))

    def do_auth(self):
        # TODO: hash the shared secret
        self.send("SWCZ/1.0; AUTH:{}".format(self.shared_key))

    def send(self, msg):
        # TODO: encrypt
        self.socket.send(msg)

    def handle_response(self, msg):
        if self.state == "INIT":
            try:
                parsed_msg = InitMsgHeader.parser().parse_string(msg, eof=True)
            except ParseError:
                self.close()
                return

            S = parsed_msg.init_clause().props()["S"]
            self.session_key = pow(S, self.secret_int, self.p)
            self.state = "AUTH"

            if self.is_server:
                self.do_handshake()
            else:
                self.do_auth()
        elif self.state == "AUTH":
            try:
                parsed_msg = AuthMsgHeader.parser().parse_string(msg, eof=True)
            except ParseError:
                self.close()
                return

            shared_key = parsed_msg.strip_header(msg)
            if not shared_key == self.shared_key:
                self.close()
                return

            if self.is_server:
                self.do_auth()

            self.state = "MSG"
        elif self.state == "MSG":
            pass

        self.frame.add_message("Them", msg)

    def close(self):
        self.socket.close()
