import select, socket
from Queue import Queue
from threading import Thread
from abc import ABCMeta, abstractmethod

EOF = '\x04'
DER = '\\'


class ResponseHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_response(self, message): pass


class MessageLogger:
    __metaclass__ = ABCMeta

    @abstractmethod
    def log(self, messsage): pass


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
        self.stopped = False

    def stop(self):
        self.stopped = True
        print("stopping response thread...")

    def run(self):
        message = ''
        while True:
            if self.stopped:
                print("response thread stopped.")
                return
            try:
                rlist, wlist, xlist = select.select([self.swcz.socket], [], [], 1.0)
                if len(rlist) == 0:
                    continue
                buff = self.swcz.socket.recv(1024)
                if len(buff) == 0:
                    self.stop()
                    self.swcz.handle_disconnect()
                    continue
            except Exception as e:
                print(str(e))
                return
            eof_index = get_eof_index(buff, message)
            if eof_index == -1:
                message += buff
            else:
                message += buff[:eof_index]
                self.swcz.handle_recv(message)
                message = buff[eof_index + 1:]


class SWCZSocket(object):
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
        self.logger = None
        self.response_thread = None
        self.queue_mode = False
        self.message_queue = Queue()

    def set_logger(self, logger):
        self.logger = logger

    def do_handshake(self):
        """ Performs the initialization and authentication of the channel """
        pass  # TODO

    def listen_async(self, handler):
        self.handler = handler
        self.response_thread = ResponseThread(self)
        self.response_thread.start()

    def send(self, message):
        if self.queue_mode:
            self.message_queue.put(message)
            print("message added to queue. press continue...")
        else:
            self._send(message)

    def _send(self, message):
        self.socket.send(message + EOF)  # TODO do encryption
        self.log("SENT:'{}'".format(message))

    def advance_queue(self):
        if not self.message_queue.empty():
            self._send(self.message_queue.get_nowait())

    def handle_recv(self, message):
        self.log("RECV:'{}'".format(message))

        if self.handler is not None:
            self.handler.handle_response(message)

    def handle_disconnect(self):
        self.log("DISCONNECTED")

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def close(self):
        print("stopping thread")
        if self.response_thread:
            self.response_thread.stop()
        print("closing socket...")
        self.socket.close()
        print("closed socket")
