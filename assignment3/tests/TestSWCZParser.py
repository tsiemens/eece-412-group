import unittest
from modgrammar import ParseError
import base64

from assignment3.SWCZParser import *


class TestSWCZParser(unittest.TestCase):

    def test_Integer(self):
        result = Integer.parser().parse_string('123', eof=True)
        self.assertEquals(str(result), '123')

    def test_Integer_not(self):
        with self.assertRaises(ParseError):
            Integer.parser().parse_string('abc', eof=True)

    def test_Integer_real(self):
        result = Integer.parser().parse_string('123.45', eof=True)
        self.assertEquals(str(result), '123')

    def test_Double(self):
        result = Double.parser().parse_string('123.45', eof=True)
        self.assertEquals(str(result), '123.45')

    def test_Double_not(self):
        with self.assertRaises(ParseError):
            Double.parser().parse_string('abc', eof=True)

    def test_Double_int(self):
        with self.assertRaises(ParseError):
            Double.parser().parse_string('123', eof=True)

    def test_version(self):
        result = Version.parser().parse_string("SWCZ/1.0\nstuff", eof=True)
        self.assertEquals(str(result), "SWCZ/1.0")

    def test_IntProp(self):
        result = IntProp.parser().parse_string("pp = 45,m", eof=True)
        self.assertEquals(str(result), "pp = 45")

    def test_IntProp2(self):
        result = IntProp.parser().parse_string("p=4,m", eof=True)
        self.assertEquals(str(result), "p=4")

    def test_IntProp_noval(self):
        with self.assertRaises(ParseError):
            IntProp.parser().parse_string("p=,", eof=True)

    def test_IntProp_noname(self):
        with self.assertRaises(ParseError):
            IntProp.parser().parse_string("=4,", eof=True)

    def test_IntPropList(self):
        result = IntPropList.parser().parse_string("pp = 45,m", eof=True)
        self.assertEquals(str(result), "pp = 45")

    def test_IntPropList2(self):
        result = IntPropList.parser().parse_string("pp = 45,m=5,n=", eof=True)
        self.assertEquals(str(result), "pp = 45,m=5")

    def test_IntPropList3(self):
        result = IntPropList.parser().parse_string("p=4, m=9 ,n=45", eof=True)
        self.assertEquals(result.props(), {'p': 4, 'm': 9, 'n': 45})
 
    def test_IntPropList3(self):
        result = IntPropList.parser().parse_string("p=4, m=9 ,k={:s},n=45".format(base64.b64encode("test")), eof=True)
        self.assertEquals(result.props(), {'p': 4, 'm': 9, 'k': "test", 'n': 45})

    def test_IntProp_noval2(self):
        result = IntPropList.parser().parse_string("p=3,m=,m=3", eof=True)
        self.assertEquals(result.props(), {'p': 3})

    def test_IntProp_noname2(self):
        with self.assertRaises(ParseError):
            IntProp.parser().parse_string("=4,m=4", eof=True)

    def test_Init(self):
        result = InitClause.parser().parse_string("INIT:p=4 , g=9,A=45",
                                                  eof=True)
        self.assertEquals(result.props(), {'p': 4, 'g': 9, 'A': 45})

    def test_Auth(self):
        result = AuthClause.parser().parse_string("AUTH: abc ed ", eof=True)

    def test_InitMsg(self):
        result = InitMsgHeader.parser().parse_string(
            "SWCZ/1.0; INIT:p=4, g=9, A=45",
            eof=True
        )
        self.assertEquals(
            result.init_clause().props(),
            {'p': 4, 'g': 9, 'A': 45}
        )

    def test_AuthMsg(self):
        msg = "SWCZ/1.0; AUTH: some text \n "
        result = AuthMsgHeader.parser().parse_string(msg, eof=True)
        self.assertEquals(result.strip_header(msg), " some text \n ")

    def test_Msg(self):
        msg = "SWCZ/1.0; UPDATE_KEY; MSG: some text \n "
        result = MsgHeader.parser().parse_string(msg, eof=True)
        self.assertTrue(result.should_update_key())
        self.assertEquals(result.strip_header(msg), " some text \n ")

    def test_MsgNoUpdate(self):
        msg = "SWCZ/1.0;MSG: some text \n "
        result = MsgHeader.parser().parse_string(msg, eof=True)
        self.assertFalse(result.should_update_key())
        self.assertEquals(result.strip_header(msg), " some text \n ")

if __name__ == '__main__':
    unittest.main()
