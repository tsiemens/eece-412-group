import hmac
import hashlib



class MessageAuthenticator(object):
    def __init__(self, key):
        self.key = key

    def sign(self, plaintext):
        """ Signs the plaintext and appends the hmac; Ready for encryption """
        return plaintext + self.compute_digest(plaintext)

    def verify(self, hashed_plaintext):
        """ Parses the plaintext from the hmac and verifies authenticity """
        plaintext = self.get_message(hashed_plaintext)
        if plaintext:
            other_hmac = hashed_plaintext[-128:]
            our_hmac = self.compute_digest(plaintext)
            return other_hmac == our_hmac
            # TODO: Figure out where to get timing attack resistance digest compare
            # TODO: Shown as present in python 2.7.8?
            # return hmac.compare_digest(other_hmac, our_hmac)
        return None

    def get_message(self, hashed_plaintext):
        """ Parses the plaintext from the hmac """
        if len(hashed_plaintext) > 128:
            return hashed_plaintext[:-128]
        return False

    def compute_digest(self, plaintext):
        return hmac.new(self.key, plaintext, hashlib.sha512).hexdigest()
