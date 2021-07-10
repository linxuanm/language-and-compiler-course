import functools

from day1_lexer import TokenType, ParserError

from .ast import *


# despite the prevalence of production rules whose first set length is 1,
# a first set is still established for illustration purposes
FIRST_SET = {
    'identifier': {TokenType.IDENTIFIER},
    'literal': {TokenType.LITERAL},
    'exp': {TokenType.LITERAL, TokenType.IDENTIFIER},
    'if': {'if'},
    'while': {'while'},
    'declare': {'decl'},
    'return': {'return'},
    'break': {'break'},
    'continue': {'continue'},
}
FIRST_SET['assign'] = FIRST_SET['identifier']
FIRST_SET['decl_func'] = FIRST_SET['identifier']
FIRST_SET['program'] = FIRST_SET['decl_func'].union(FIRST_SET['declare'])
FIRST_SET['stmt'] = functools.reduce(lambda a, b: a.union(b), [
    FIRST_SET[i] for i in (
        'if', 'while', 'declare', 'assign',
        'return', 'break', 'continue', 'exp'
    )
])


class Reader:
    """
    A class that handles the reading, incrementing and restoring of the
    token position while parsing.
    """

    def __init__(self, tokens: [(str, TokenType)]):
        self.tokens = tokens
        self.pos = 0
        self.len = len(tokens)

    def match(self, matcher) -> str:
        """
        Increments if matcher matches either the content or the type of the
        upcoming token, otherwise throws a ParserError.

        Returns the content of the token.
        """

        if type(matcher) not in (str, TokenType):
            raise ValueError(f'Matcher must be of type str or TokenType')

        if self.pos >= self.len:
            raise ParserError('End of token sequence')

        upcoming = self.tokens[self.pos]
        if matcher not in upcoming:
            raise ParserError(
                f'Token {upcoming}  does not match the '
                f'expected "{matcher}"'
            )

        self.pos += 1
        return upcoming[0]

    def test(self, matcher) -> bool:
        """
        Returns true if matcher matches either the content or the type of the
        upcoming token, otherwise returns false.
        """

        if type(matcher) not in (str, TokenType):
            raise ValueError(f'Matcher must be of type str or TokenType')

        if self.pos >= self.len:
            return False

        return matcher in self.tokens[self.pos]

    def test_set(self, first_set: set) -> bool:
        """
        Tests whether the next token is in the given first set.
        Behaves similarly to Reader.test
        """

        for i in first_set:
            if self.test(i):
                return True

        return False

    def peek(self) -> (str, TokenType):
        """
        Returns the next token. No increments.
        Raises a ParserError if the token list is fully consumed.

        Should not be used unless for debugging purposes.
        """
        if self.pos >= self.len:
            raise ParserError('End of token sequence')

        return self.tokens[self.pos]

    def end(self) -> bool:
        return self.pos >= self.len


from .exp_parser import parse_exp


def parse(reader: Reader) -> Program:
    """
    Parses an entire program. This one is already written for you.

    Note: although it is more efficient to just Reader.test with increment
    and remove the parsing for the first token for each production, the
    general "check for first set and recursively parse the entire" is
    incorporated for generalizability and simplicity.
    """

    glob_decl = []

    while reader.test_set(FIRST_SET['program']):
        if reader.test_set(FIRST_SET['declare']):
            glob_decl.append(parse_declare(reader))
        elif reader.test_set(FIRST_SET['decl_func']):
            glob_decl.append(parse_func_decl(reader))
        else:
            raise ParserError(
                f'Unexpected token {reader.peek()} '
                'encountered in the global scope'
            )

    if not reader.end():
        raise ParserError(
            f'Remaining unstructured token beginning with {reader.peek()}'
        )

    return Program(glob_decl)


def parse_declare(reader: Reader) -> Declare:
    """
    Parses a variable declaration statement (e.g. 'decl a, b;').
    """

    vars = []
    reader.match('decl')

    if reader.test(TokenType.IDENTIFIER):
        vars.append(reader.match(TokenType.IDENTIFIER))

        while reader.test(','):
            reader.match(',')
            vars.append(reader.match(TokenType.IDENTIFIER))

    reader.match(';')

    return Declare(vars)


def parse_func_decl(reader: Reader) -> FuncDecl:
    """
    Parses a function declaration.
    """

    name = reader.match(TokenType.IDENTIFIER)
    params = []
    code = []

    reader.match('(')

    if reader.test(TokenType.IDENTIFIER):
        params.append(reader.match(TokenType.IDENTIFIER))

        while reader.test(','):
            reader.match(',')
            params.append(reader.match(TokenType.IDENTIFIER))

    reader.match(')')
    reader.match('{')

    while reader.test_set(FIRST_SET['stmt']):
        code.append(parse_statement(reader))

    reader.match('}')

    return FuncDecl(name, params, code)

def parse_statement(reader) -> Stmt:
    """
    Parses a statement (stmt).
    Can be any of 'if', 'while', 'declare', 'assign', 'return', 'break',
    'continue' or 'exp'.
    """

    if reader.test_set(FIRST_SET['if']):
        pass

    elif reader.test_set(FIRST_SET['while']):
        pass

    elif reader.test_set(FIRST_SET['declare']):
        return parse_declare(reader)

    elif reader.test_set(FIRST_SET['assign']):
        pass

    elif reader.test_set(FIRST_SET['return']):
        reader.match('return')
        exp = parse_exp(reader)
        return Return(exp)

    elif reader.test_set(FIRST_SET['break']):
        reader.match('break')
        return Break()

    elif reader.test_set(FIRST_SET['continue']):
        reader.match('continue')
        return Continue()

    elif reader.test_set(FIRST_SET['exp']):
        return parse_exp(reader)

    else:
        raise ParserError(
            f'Unexpected token {reader.peek()} encountered'
            'while parsing statement'
        )