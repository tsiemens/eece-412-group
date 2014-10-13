from math import factorial
from modgrammar import ParseError
from Crypto.Random.random import randint

from MessageCryptoSystem import MessageCryptoSystem
from AsyncMsgSocket import AsyncMsgSocket
from SWCZParser import InitMsgHeader, AuthMsgHeader, MsgHeader

class AuthenticationError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


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
        self.session_crypto = None
        self.state = "INIT"

        self.socket = AsyncMsgSocket(frame, sock)
        self.socket.listen_async(self)

        if not is_server:
            self.do_handshake()

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        A = pow(self.g, self.secret_int, self.p)
        self._send("SWCZ/1.0; INIT:  S={}".format(A))

    def do_auth(self):
        # TODO: hash the shared secret
        self._send("SWCZ/1.0; AUTH:{}".format(self.shared_key))

    def do_send_msg(self, msg):
        # TODO decide on update key
        self._send("SWCZ/1.0; MSG:{}".format(msg))
        self.frame.add_message("Me", msg)
    
    def _send(self, msg):
        # TODO: encrypt - taken care of
        self.message_crypto = MessageCryptoSystem(self.session_key, self.shared_key)
        self.socket.send(msg, plaintext=self.message_crypto.wrap_message(msg))
    
    def send(self, msg):
        if self.state == "MSG":
            self.do_send_msg(msg)

    def handle_response(self, msg):
        try:
            if self.state == "INIT":
                parsed_msg = InitMsgHeader.parser().parse_string(msg, eof=True)
                S = parsed_msg.init_clause().props()["S"]
                self.session_key = pow(S, self.secret_int, self.p)
                self.state = "AUTH"

                if self.is_server:
                    self.do_handshake()
                else:
                    self.do_auth()

            elif self.state == "AUTH":
                parsed_msg = AuthMsgHeader.parser().parse_string(msg, eof=True)
                shared_key = parsed_msg.strip_header(msg)
                if not shared_key == self.shared_key:
                    raise AuthenticationError(
                        "Failed to authenticate: {} != {}".format(
                            self.shared_key, shared_key))

                if self.is_server:
                    self.do_auth()

                self.state = "MSG"
                self.socket.queue_mode = False
            elif self.state == "MSG":
                # TODO decrypt - taken care of
                # TODO check hmac - taken care of
                parsed_msg = MsgHeader.parser().parse_string(msg, eof=True)
                # TODO parsed_msg.should_update_key()
                chat_msg = parsed_msg.strip_header(msg)
                self.frame.add_message("Them", chat_msg)

        except (ParseError, AuthenticationError) as e:
            print(str(e))
            self.close()

    def close(self):
        self.socket.close()
