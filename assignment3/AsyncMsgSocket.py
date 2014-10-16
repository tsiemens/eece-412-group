import select
import base64
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
from threading import Thread

EOF = '\x04'


def get_eof_index(buff):
    for i in range(0, len(buff)):
        if buff[i] == EOF:
            return i
    return -1


class ResponseThread(Thread):
    def __init__(self, asocket):
        super(ResponseThread, self).__init__()
        self.asocket = asocket
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
                rlist, wlist, xlist = select.select(
                    [self.asocket.socket],
                    [],
                    [],
                    1.0
                )
                if len(rlist) == 0:
                    continue
                buff = self.asocket.socket.recv(1024)
                if len(buff) == 0:
                    self.stop()
                    self.asocket.handle_disconnect()
                    continue
            except Exception as e:
                print(str(e))
                return
            eof_index = get_eof_index(buff)
            if eof_index == -1:
                message += buff
            else:
                message += buff[:eof_index]
                self.asocket.handle_recv(message)
                message = buff[eof_index + 1:]


class AsyncMsgSocket(object):
    """ An event based socket wrapper. Messages are Base64 encoded, and
        terminated with an EOF character. """

    def __init__(self, frame, sock):
        self.frame = frame
        self.socket = sock
        self.response_thread = None
        self.queue_mode = True
        self.message_queue = Queue()

    def listen_async(self, handler):
        """ handler must implement handle_response(self, msg) """
        self.handler = handler
        self.response_thread = ResponseThread(self)
        self.response_thread.start()

    def send(self, message, plaintext=None):
        if self.queue_mode:
            self.message_queue.put((message, plaintext))
            self.frame.append_button_queue(True)
            print("message added to queue. press continue...")
        else:
            self._send((message, plaintext))

    def _send(self, msg_and_plain):
        # here base64 is used so EOF will never occur elsewhere
        self.socket.send(base64.b64encode(msg_and_plain[0]) + EOF)
        self.frame.append_debug_queue("SENT:'{}'\n(Plain:'{}')".format(hexstring(msg_and_plain[0]), msg_and_plain[1]))

    def advance_queue(self):
        if not self.message_queue.empty():
            self._send(self.message_queue.get_nowait())
            if self.message_queue.empty():
                self.frame.append_button_queue(False)

    def handle_recv(self, message):
        message = base64.b64decode(message)
        self.frame.append_debug_queue("RECV:'{}'".format(hexstring(message)))

        if self.handler is not None:
            self.handler.handle_response(message)

    def handle_disconnect(self):
        self.frame.append_debug_queue("DISCONNECTED")

    def close(self):
        if self.response_thread:
            self.response_thread.stop()
        self.socket.close()
        self.handle_disconnect()
        print("closed socket")


def hexstring(s):
    s = str(s)
    return ":".join("{:02x}".format(ord(c)) for c in s)
