import unittest
import hashlib, hmac
from assignment3.Message import *

class TestMessage(unittest.TestCase):

    def setUp(self):
        self.message = Message("1234", "test")

    def test_sign(self):
        signed_message = self.message.sign()
        self.assertEquals(signed_message, "test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")

    def test_get_message(self):
        message = Message("1234", "test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")
        self.assertEquals(message.get_message(), "test")

    def test_verify(self):
        message = Message("1234", "test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")
        self.assertTrue(message.verify())

    def test_verify_bad(self):
        message = Message("1234", "test571f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")
        self.assertFalse(message.verify())

    def test_verify_short(self):
        message = Message("1234", "b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")
        self.assertFalse(message.verify())

    def test_compute_digest(self):
        digest = Message.compute_digest(self.message.key, self.message.string)
        self.assertEquals(digest, "471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")

if __name__ == '__main__':
    unittest.main()
