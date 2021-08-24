import functools

from day1_lexer import TokenType, ParserError

from .ast import *


# despite the prevalence of production rules whose first set length is 1,
# a first set is still established for illustration purposes
FIRST_SET = {
    'identifier': {TokenType.IDENTIFIER},
    'literal': {TokenType.LITERAL},
    'imm_exp': {TokenType.LITERAL, TokenType.IDENTIFIER},
    'if': {'if'},
    'while': {'while'},
    'declare': {'decl'},
    'return': {'return'},
    'break': {'break'},
    'continue': {'continue'},
    'unop_exp': {'-', '!'},
    'paren_exp': {'('},
    'iden_start': {TokenType.IDENTIFIER} # left factors assign and exp
}
FIRST_SET['assign'] = FIRST_SET['identifier']
FIRST_SET['decl_func'] = FIRST_SET['identifier']
FIRST_SET['program'] = FIRST_SET['decl_func'].union(FIRST_SET['declare'])
FIRST_SET['exp'] = functools.reduce(set.union, [
    FIRST_SET[i] for i in ('imm_exp', 'unop_exp', 'paren_exp')
])
FIRST_SET['stmt'] = functools.reduce(set.union, [
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

    def back(self) -> None:
        """
        Don't use this. It doesn't belong in LL(1) parsers.
        """

        self.pos -= 1

    def end(self) -> bool:
        return self.pos >= self.len


def parse(reader: Reader) -> Program:
    """
    Parses an entire program. This one is already written for you.

    Note: although it is more efficient to just Reader.test with increment
    and remove the parsing for the first token for each production, the
    general "check for first set and recursively parse the entire" is
    incorporated for generalizability and simplicity.
    """

    raise NotImplementedError


def parse_statement_list(reader: Reader) -> [Stmt]:
    """
    Parses 0 or more statements and returns them as a list.
    """

    code = []

    while reader.test_set(FIRST_SET['stmt']):
        code.append(parse_statement(reader))

    return code


def parse_identifier_list(reader: Reader) -> [str]:
    """
    Parses 0 or more identifiers and returns them as a list.
    """

    names = []

    if reader.test_set(FIRST_SET['identifier']):
        names.append(reader.match(TokenType.IDENTIFIER))

        while reader.test(','):
            reader.match(',')
            names.append(reader.match(TokenType.IDENTIFIER))

    return names

def parse_exp_list(reader: Reader) -> [Exp]:
    """
    Parses 0 or more expressions and returns them as a list.
    """

    exps = []

    if reader.test_set(FIRST_SET['exp']):
        exps.append(parse_exp(reader))

        while reader.test(','):
            reader.match(',')
            exps.append(parse_exp(reader))

    return exps


def parse_declare(reader: Reader) -> Declare:
    """
    Parses a variable declaration statement (e.g. 'decl a, b;').
    """

    reader.match('decl')
    vars = parse_identifier_list(reader)
    reader.match(';')

    return Declare(vars)


def parse_func_decl(reader: Reader) -> FuncDecl:
    """
    Parses a function declaration.
    """

    raise NotImplementedError


def parse_if(reader: Reader) -> If:
    """
    Parses an if statement.

    The returned value contains an empty 'else' code block if there is no 'else' clause attached to the 'if' construct.
    """

    reader.match('if')

    reader.match('(')
    cond = parse_exp(reader)
    reader.match(')')

    reader.match('{')
    if_code = parse_statement_list(reader)
    reader.match('}')

    # 'else' clause
    #
    # technically 'else' should be left factored out into another production
    # rule, but since 'else' is the only production whose terminal has an
    # optional suffix in our grammar, it is probably simpler to just make
    # this as an exception and not create a dedicated 'FIRST_SET' entry
    else_code = []
    if reader.test('else'):
        reader.match('else')
        reader.match('{')
        else_code = parse_statement_list(reader)
        reader.match('}')

    return If(cond, if_code, else_code)


def parse_while(reader: Reader) -> While:
    """
    Parses a while loop. Should be pretty trivial after completing 'parse_if'.
    """

    raise NotImplementedError


def parse_identifier_start(reader: Reader) -> Stmt:
    """
    Used to resolve ambiguity between assign and exp.

    assign = identifier, "=", exp, ";";
    var_exp = identifier;
    func_call = identifier, '(', exp_list, ')';

    As you can see, all of the above begins with an identifier, and since

    stmt = ... | exp;

    , there is an indirect ambiguity induced by identical starting token.

    Luckily this is trivial to fix; just left factor.
    """

    # nested since this is not used elsewhere
    def partial_parse_assign(name, reader):
        reader.match('=')
        value = parse_exp(reader)
        reader.match(';')

        return Assign(name, value)

    # note: there should be NO backtracking in LL(1) parsers
    # however, left factoring the exp production makes the code less
    # straightforward, which is something that I want to avoid in this course
    def backtrack_and_parse_exp(reader):
        reader.back()
        return parse_exp(reader)

    name = reader.match(TokenType.IDENTIFIER)

    if reader.test('='):
        return partial_parse_assign(name, reader)

    else:
        value = backtrack_and_parse_exp(reader)
        reader.match(';')
        return ExpStmt(value)


def parse_statement(reader: Reader) -> Stmt:
    """
    Parses a statement (stmt).
    Can be any of 'if', 'while', 'declare', 'assign', 'return', 'break',
    'continue' or 'exp'.
    """

    # since we aren't using a LL(1) table for complexity concerns, we use
    # if/else to accomplish the same idea
    #
    # note that the idea of 'checking if the FIRST_SET contains the next token
    # and then explicitly matching only one specific token' does not make much
    # sense programmatically; however, in this case we are demontrating the
    # deriving of a production from another given the starting token, and
    # therefore we abstracts everything inside each 'if' switch as simply
    # something that parses the given production derived from the tested
    # FIRST_SET

    raise NotImplementedError


from .exp_parser import parse_exp