import unittest
import socket
from threading import Thread
from SWCZSocket import *
import time

PORT = 55555 # Arbitrary non-privileged port

class ClientThread(Thread):
    def __init__(self):
        HOST = 'localhost'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

class Test1Thread(ClientThread):
    def run(self):
        self.socket.sendall('foo' + EOF)

class TestHandler(ResponseHandler):
    def __init__(self, swczsock):
        self.sock = swczsock

    def handle(self, message):
        print('Recieved ' + message)
        self.sock.close()

class SWCZSocketTest(unittest.TestCase):

    def setUp(self):
        HOST = '' # Symbolic name meaning all available interfaces
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)

    def test_async_recieve(self):
        thread = Test1Thread()
        conn, addr = self.socket.accept()
        thread.run()
        
        swcz = SWCZSocket(conn, 2, 4, 6, "shared", True)
        handler = TestHandler(swcz)
        swcz.listen_async(handler)
        time.sleep(0.2)
        self.socket.close()

class SWCZSocketUtilsTest(unittest.TestCase):
    
    def test_is_char_derefed_yes1(self):
        buff = 'foo' + DER + EOF
        msg = ''
        self.assertTrue(is_char_derefed(buff, 4, msg) is True)

    def test_is_char_derefed_yes2(self):
        buff = DER + DER + EOF
        msg = 'foo' + DER + DER + DER
        self.assertTrue(is_char_derefed(buff, 2, msg) is True)
    
    def test_is_char_derefed_no1(self):
        buff = 'foo' + DER + DER + EOF
        msg = ''
        self.assertTrue(is_char_derefed(buff, 5, msg) is False)

    def test_is_char_derefed_no2(self):
        buff = DER + DER + EOF
        msg = 'foo'
        self.assertTrue(is_char_derefed(buff, 2, msg) is False)

    def test_is_char_derefed_no3(self):
        buff = 'foo' + EOF
        msg = ''
        self.assertTrue(is_char_derefed(buff, 3, msg) is False)

    def test_get_eof_index_none(self):
        buff = 'foo'
        msg = ''
        self.assertEquals(get_eof_index(buff, msg), -1)
    
    def test_get_eof_index(self):
        buff = 'foo' + EOF + "bar"
        msg = ''
        self.assertEquals(get_eof_index(buff, msg), 3)

    def test_get_eof_index_derefed(self):
        buff = 'foo' + DER + EOF + "bar" + EOF
        msg = ''
        self.assertEquals(get_eof_index(buff, msg), 8)

    def test_get_eof_index_derefed2(self):
        buff = EOF + "bar" + EOF
        msg = 'foo' + DER
        self.assertEquals(get_eof_index(buff, msg), 4)


if __name__ == '__main__':
    unittest.main()
