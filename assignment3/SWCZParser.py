from modgrammar import *


grammar_whitespace_mode = 'explicit'


class Integer(Grammar):
    grammar = (WORD("0-9"))


class Double(Grammar):
    grammar_whitespace_mode = 'explicit'
    grammar = (Integer, '.', Integer)


class Version(Grammar):
    grammar_whitespace_mode = 'explicit'
    grammar = (L("SWCZ/"), Double)


class IntProp(Grammar):
    grammar_whitespace_mode = 'optional'
    grammar = (WORD("a-zA-Z_"), L("="), Integer)

    def pair(self):
        return (str(self[0]), int(str(self[2])))


class IntPropList(Grammar):
    grammar_whitespace_mode = 'optional'
    grammar = (IntProp, ZERO_OR_MORE(L(","), IntProp))

    def props(self):
        pair = self[0].pair()
        pairs = {pair[0]: pair[1]}
        for e in self.elements[1]:
            pair = e[1].pair()
            pairs[pair[0]] = pair[1]
        return pairs


class InitClause(Grammar):
    grammar_whitespace_mode = 'optional'
    grammar = (L("INIT"), L(':'), IntPropList)

    def props(self):
        return self[2].props()


class AuthClause(Grammar):
    grammar = (L("AUTH"), L(":"))


class Header(Grammar):
    grammar_whitespace_mode = 'optional'

    def strip_header(self, msg):
        return msg[len(str(self)):]


class InitMsgHeader(Header):
    grammar = (Version, ';', InitClause)

    def init_clause(self):
        return self[2]


class AuthMsgHeader(Header):
    grammar = (Version, L(';'), AuthClause)


class MsgHeader(Header):
    grammar = (Version, L(';'), OPTIONAL(L("UPDATE_KEY"), L(";")), L('MSG:'))

    def should_update_key(self):
        optional = self[2]
        if isinstance(optional, Grammar):
            return str(optional[0]) == "UPDATE_KEY"

        return False
