import unittest
import socket
from threading import Thread
from assignment3.AsyncMsgSocket import *
import time


PORT = 55555  # Arbitrary non-privileged port

class DummyFrame(object):
    def log(self, msg):
        pass


class ClientThread(Thread):
    def __init__(self):
        HOST = 'localhost'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        self.asock = AsyncMsgSocket(DummyFrame(), sock)
        self.asock.queue_mode = False


class Test1Thread(ClientThread):
    def run(self):
        self.asock.send('foo\x04bar')


class TestHandler(object):
    def __init__(self, asock):
        self.asock = asock
        self.passed = False

    def handle_response(self, message):
        expected = 'foo\x04bar'
        self.passed = message == expected
        if not self.passed:
            print("expected {} but got {}".format(expected, message))
        self.asock.close()


class TestAsyncMsgSocket(unittest.TestCase):

    def setUp(self):
        HOST = ''  # Symbolic name meaning all available interfaces
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)

    def test_async_send_recieve(self):
        thread = Test1Thread()
        conn, addr = self.socket.accept()
        thread.run()

        asock = AsyncMsgSocket(DummyFrame(), conn)
        asock.queue_mode = False
        handler = TestHandler(asock)
        asock.listen_async(handler)
        time.sleep(0.2)
        self.assertTrue(handler.passed)
        self.socket.close()


class TestAsyncMsgSocketUtils(unittest.TestCase):

    def test_get_eof_index(self):
        buff = 'foo' + EOF + "bar"
        self.assertEquals(get_eof_index(buff), 3)

    def test_get_eof_index_2(self):
        buff = 'foo' + EOF + "bar" + EOF
        self.assertEquals(get_eof_index(buff), 3)

    def test_get_eof_index_3(self):
        buff = "foo bar" + EOF
        self.assertEquals(get_eof_index(buff), 7)

    def test_get_eof_index4(self):
        buff = EOF + "foo bar"
        self.assertEquals(get_eof_index(buff), 0)


if __name__ == '__main__':
    unittest.main()
