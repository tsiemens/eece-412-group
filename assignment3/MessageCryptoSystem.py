from MessageCrypto import *
from MessageAuthenticator import *


class MessageCryptoSystem(object):
    def __init__(self, session_key, shared_key):
        """" Initialize the Message cryptosystem with a
             128 byte session key (16 Chars) and a
             shared key """
        self.shared_key = shared_key
        self.session_key = session_key
        self.crypto = MessageCrypto(session_key)
        self.auth = MessageAuthenticator(shared_key)

    def wrap_message(self, plaintext):
        """ Prepares signed, encrypted, and signed message """
        signed = self.auth.sign(plaintext)
        encrypted = self.crypto.encrypt(signed)
        return self.auth.sign(encrypted)

    def unwrap_message(self, ciphertext):
        """ Returns plaintext from message """
        if self.auth.verify(ciphertext):
            decrypted = self.crypto.decrypt(self.auth.get_message(ciphertext))
            if self.auth.verify(decrypted):
                return self.auth.get_message(decrypted)
        return None
