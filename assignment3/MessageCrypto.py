from Crypto.Cipher import AES
import os
import base64


class MessageCrypto(object):
    def __init__(self, key):
        """" Initialize the Message cryptosystem with a 128 byte key (16 Chars) """
        self.key = key

    def encrypt(self, plaintext):
        """ Returns ciphertext prepended by IV - Base64 Encoded """
        iv = os.urandom(16)
        crypto_system = self._init_crypto_system(iv)
        return iv + crypto_system.encrypt(self._pad_message(plaintext))

    def decrypt(self, ciphertext):
        """ Returns plaintext from ciphertext, prepended by IV - Base64 Encoded """
        # binary_ciphertext = base64.b64decode(ciphertext)
        binary_ciphertext = ciphertext
        crypto_system = self._init_crypto_system(binary_ciphertext[:16])
        plaintext = crypto_system.decrypt(binary_ciphertext[16:])
        return self._unpad_message(plaintext)

    def _init_crypto_system(self, iv):
        """ Initializes a cryptosystem for encryption and decryption """
        return AES.new(self.key, AES.MODE_CBC, iv)

    def _pad_message(self, plaintext):
        """ Pads plaintext with newline characters, to a round 16 bytes """
        pad_count = len(plaintext) % 16
        padding = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n'

        if (pad_count != 0):
            return plaintext + padding[:(16 - pad_count)]
        else:
            return plaintext

    def _unpad_message(self, plaintext):
        """ Removes trailing newline characters """
        return plaintext.rstrip()
