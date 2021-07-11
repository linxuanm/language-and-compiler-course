import typing

from day1_lexer import TokenType, ParserError

from .ast import *
from .parser import FIRST_SET, Reader, parse_exp_list


def parse_exp(reader: Reader) -> Exp:
    return parse_product(reader)


def parse_product(reader: Reader) -> Exp:
    """
    Parses an infix operation whose precedence is the same as 'mul' and 'div'.

    Check source_grammar.cf for a definitive grammar guide. Note the
    elimination of left recursions.
    """

    def parse_partial(reader: Reader) -> typing.Callable[[Exp], Exp]:
        # since there is no AST node directly corresponding to the eliminated
        # version of a binary operation, a bit of currying is used here for
        # generalizablity

        if not reader.test_set({'*', '/'}):
            return lambda x: x

        symbol = reader.match(TokenType.OPERATOR)
        end_exp = parse_exp_imm(reader)

        tail = parse_partial(reader)
        build = lambda start, sym=symbol, end=end_exp: BinOp(sym, start, end)

        return lambda x: tail(build(x))

    start_exp = parse_exp_imm(reader) # non-recursive non-terminals

    return parse_partial(reader)(start_exp)


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
        return UnOp(reader.match(TokenType.OPERATOR), parse_exp(reader))

    elif reader.test_set(FIRST_SET['identifier']):
        name = reader.match(TokenType.IDENTIFIER)

        if reader.test('('):
            reader.match('(')
            params = parse_exp_list(reader)
            reader.match(')')

            return FuncCall(name, params)

        return VarExp(name)

    elif reader.test_set(FIRST_SET['paren_exp']):
        reader.match('(')
        value = parse_exp(reader)
        reader.match(')')

        return value