import unittest
from assignment3.MessageCryptoSystem import *
from assignment3.MessageCrypto import *
from assignment3.MessageAuthenticator import *

class TestMessageCryptoSystem(unittest.TestCase):

    def setUp(self):
        self.crypto_system = MessageCryptoSystem('1111111111111111', 'some_shared_key')
        self.crypto = MessageCrypto('1111111111111111')
        self.authenticator = MessageAuthenticator('some_shared_key')

    def test_wrap_unwrap(self):
        self.assertEqual(self.crypto_system.unwrap_message(self.crypto_system.wrap_message('test')), 'test')

    def test_wrap_bad_inner_signature(self):
        message = self.bad_inner_signature('test')
        self.assertNotEqual(self.crypto_system.wrap_message('test'), message)

    def test_wrap_bad_outer_signature(self):
        message = self.bad_outer_signature('test')
        self.assertNotEqual(self.crypto_system.wrap_message('test'), message)

    def test_wrap_bad_crypto(self):
        message = self.bad_crypto('test')
        self.assertNotEqual(self.crypto_system.wrap_message('test'), message)

    def test_unwrap_bad_inner_signature(self):
        message = self.bad_inner_signature('test')
        self.assertNotEqual(self.crypto_system.wrap_message(message), None)

    def test_unwrap_bad_outer_signature(self):
        message = self.bad_outer_signature('test')
        self.assertNotEqual(self.crypto_system.wrap_message(message), None)

    def test_unwrap_bad_crypto(self):
        message = self.bad_crypto('test')
        try:
            self.crypto_system.unwrap_message(message)
        except TypeError, e:
            self.assertEqual(type(e), TypeError)

    def bad_crypto(self, text):
        signed_message = self.authenticator.sign(text)
        encrypted_message = self.crypto.encrypt(signed_message)
        encrypted_message = encrypted_message[:len(encrypted_message) - 1] + '0'
        return self.authenticator.sign(encrypted_message)

    def bad_inner_signature(self, text):
        signed_message = self.authenticator.sign(text)
        signed_message = signed_message[:len(signed_message) - 1] + '0'
        encrypted_message = self.crypto.encrypt(signed_message)
        return self.authenticator.sign(encrypted_message)

    def bad_outer_signature(self, text):
        signed_message = self.authenticator.sign(text)
        encrypted_message = self.crypto.encrypt(signed_message)
        message = self.authenticator.sign(encrypted_message)
        return message[:len(message) - 1] + '0'

if __name__ == '__main__':
    unittest.main()
