import hashlib, hmac

class Message(object):
    def __init__(self, key, string):
        self.key = key
        self.string = string

    def sign(self):
        """ Signs the string and appends the hmac; Ready for encryption """
        return self.string + Message.compute_digest(self.key, self.string)

    def verify(self):
        """ Parses the plaintext from the hmac and verifies authenticity """
        plaintext = self.get_message()
        if (plaintext):
            other_hmac = self.string[-128:]
            our_hmac = Message.compute_digest(self.key, plaintext)
            return other_hmac == our_hmac
            # TODO: Figure out where to get timing attack resistance digest compare
            # TODO: Shown as present in python 2.7.8?
            # return hmac.compare_digest(other_hmac, our_hmac)
        return False

    def get_message(self):
        """ Parses the plaintext from the hmac """
        if (len(self.string) > 128):
            return self.string[:-128]
        return False


    # @classmethod
    # def compute_digest(cls, key, string):
    @staticmethod
    def compute_digest(key, string):
        return hmac.new(key, string, hashlib.sha512).hexdigest()


