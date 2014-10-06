import unittest
from assignment3.MessageCrypto import *

class TestMessageCrypto(unittest.TestCase):

    def setUp(self):
        self.crypto_system = MessageCrypto('1111111111111111')

    def test_encrypt_generates_new_iv(self):
        encrypted_message_0 = self.crypto_system.encrypt('testtesttesttest')
        encrypted_message_1 = self.crypto_system.encrypt('testtesttesttest')
        self.assertNotEqual(encrypted_message_0, encrypted_message_1)

    def test_message_padding(self):
        encrypted_message_0 = self.crypto_system.encrypt('test')
        self.assertNotEqual(encrypted_message_0, None)

    def test_encrypt_decrypt(self):
        encrypted_message_0 = self.crypto_system.encrypt('test')
        self.assertEqual(self.crypto_system.decrypt(self.crypto_system.encrypt('test')), 'test')

if __name__ == '__main__':
    unittest.main()
