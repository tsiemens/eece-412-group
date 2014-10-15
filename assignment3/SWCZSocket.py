from math import factorial
from modgrammar import ParseError
from Crypto.Random.random import randint
import hmac
import hashlib
import base64

from MessageCryptoSystem import MessageCryptoSystem
from AsyncMsgSocket import AsyncMsgSocket
from SWCZParser import InitMsgHeader, HelloMsgHeader, MsgHeader


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
        self.their_nonce = None
        self.my_nonce = str(randint(0, pow(2, 256)))
        self.session_key = None
        self.session_crypto = None
        self.state = "HELLO"

        self.socket = AsyncMsgSocket(frame, sock)
        self.socket.listen_async(self)

        if not is_server:
            self.do_handshake()
            self.state = "INIT"

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        print("Sending Hello Message")
        self._send_unencrypted("SWCZ/1.0; HELLO:  N={}".format(self.my_nonce))

    def do_auth(self):
        # TODO: hash the shared secret
        print("Sending Auth Message")
        self.my_hash = hmac.new(self.their_nonce, self.shared_key, hashlib.sha512).hexdigest()
        S = pow(self.g, self.secret_int, self.p)
        #self._send_unencrypted("SWCZ/1.0; AUTH:{}".format(self.shared_key))
        if self.is_server:
            self._send_unencrypted("SWCZ/1.0; INIT: N={}, S={}, H={}".format(self.my_nonce, S, base64.b64encode(self.my_hash)))
        else:
            self._send_unencrypted("SWCZ/1.0; INIT: S={}, H={}".format(S, base64.b64encode(self.my_hash)))

    def do_send_msg(self, msg):
        # TODO decide on update key
        self._send_encrypted("SWCZ/1.0; MSG:{}".format(msg))
        self.frame.add_message("Me", msg)

    def _send_unencrypted(self, msg):
        self.socket.send(msg, plaintext=msg)

    def _send_encrypted(self, msg):
        self.socket.send(self.message_crypto.wrap_message(msg),
                         plaintext=msg)

    def send(self, msg):
        if self.state == "MSG":
            self.do_send_msg(msg)

    def handle_response(self, msg):
        try:
            if self.state == "HELLO":
                print("Server Receiving Hello Message")
                parsed_msg = HelloMsgHeader.parser().parse_string(msg, eof=True)
                self.their_nonce = str(parsed_msg.hello_clause().props()["N"])

                if self.is_server:
                    self.do_auth()

                self.state = "INIT"
            elif self.state == "INIT":
                print("Receiving Init Message")
                parsed_msg = InitMsgHeader.parser().parse_string(msg, eof=True)

                if not self.is_server:
                    self.their_nonce = str(parsed_msg.init_clause().props()["N"])

                S = parsed_msg.init_clause().props()["S"]
                hash = parsed_msg.init_clause().props()["H"]
                their_hash = hmac.new(self.my_nonce, self.shared_key, hashlib.sha512).hexdigest()

                self.session_key = str(pow(S, self.secret_int, self.p))[:32]
                self.message_crypto = MessageCryptoSystem(self.session_key,
                                                          self.shared_key)

                if not their_hash == hash:
                    raise AuthenticationError(
                        "Failed to authenticate: {} != {}".format(
                            their_hash, hash))
                if not self.is_server:
                    self.do_auth()

                self.state = "MSG"
                self.socket.queue_mode = False

            elif self.state == "MSG":
                # TODO decrypt - taken care of
                # TODO check hmac - taken care of
                raw_msg = self.message_crypto.unwrap_message(msg)

                parsed_msg = MsgHeader.parser().parse_string(raw_msg, eof=True)
                # TODO parsed_msg.should_update_key()
                chat_msg = parsed_msg.strip_header(raw_msg)
                self.frame.add_message("Them", chat_msg)

        except (ParseError, AuthenticationError) as e:
            print(str(e))
            self.close()

    def close(self):
        self.socket.close()
