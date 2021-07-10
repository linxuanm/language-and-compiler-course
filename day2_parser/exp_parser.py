from day1_lexer import TokenType, ParserError

from .ast import *
from .parser import FIRST_SET, Reader, parse_exp_list


def parse_exp(reader: Reader) -> Exp:
    return parse_exp_imm(reader)


def parse_exp_imm(reader: Reader) -> Exp:
    """
    Parses a value whose construct has no binary operators (and therefore
    of the highest precedence).
    """

    # note that the idea of 'checking if the FIRST_SET contains the next token
    # and then explicitly matching only one specific token' does not make much
    # sense programmatically; however, in this case we are demontrating the
    # deriving of a production from another given the starting token, and
    # therefore we abstracts everything inside each 'if' switch as simply
    # something that parses the given production derived from the tested
    # FIRST_SET
    if reader.test_set(FIRST_SET['literal']):
        return Literal(reader.match(TokenType.LITERAL))

    elif reader.test_set(FIRST_SET['unop_exp']):
        return Unop(reader.match(TokenType.OPERATOR), parse_exp(reader))

    elif reader.test_set(FIRST_SET['identifier']):
        name = reader.match(TokenType.IDENTIFIER)

        if reader.test('('):
            reader.match('(')
            params = parse_exp_list(reader)
            reader.match(')')

            return FuncCall(name, params)

        return VarExp(name)
