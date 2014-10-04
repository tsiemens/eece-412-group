import unittest
import hashlib, hmac
from assignment3.MessageAuthenticator import *

class TestMessageAuthenticator(unittest.TestCase):

    def setUp(self):
        self.message = MessageAuthenticator("1234")

    def test_sign(self):
        self.assertEquals(self.message.sign("test"), "test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")

    def test_get_message(self):
        self.assertEquals(self.message.get_message("test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5"), "test")

    def test_verify(self):
        self.assertTrue(self.message.verify("test471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5"))

    def test_verify_bad(self):
        self.assertFalse(self.message.verify("test571f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5"))

    def test_verify_short(self):
        self.assertFalse(self.message.verify("b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5"))

    def test_compute_digest(self):
        self.assertEquals(self.message.compute_digest("test"), "471f609bf6d8b0d6419ec68efd5453b3922560aa3f351088e35a424c30e43725c261f8e631f34cb06ca475ae678b0aa19b5b0c7690dff30b0d88e96a077203f5")

if __name__ == '__main__':
    unittest.main()
