from day1_lexer import TokenType, ParserError

from .ast import *


class Reader:
    """
    A class that handles the reading, incrementing and restoring of the
    token position while parsing.
    """

    def __init__(self, tokens: [(str, TokenType)]):
        self.tokens = tokens
        self.pos = 0
        self.len = len(tokens)

    def match(self, matcher) -> None:
        """
        Increments if matcher matches either the content or the type of the
        upcoming token, otherwise throws a ParserError.
        """

        if self.pos >= self.len:
            raise ParserError('End of token sequence')

        upcoming = self.tokens[self.pos]
        if seq not in upcoming:
            raise ParserError(
                f'Token {upcoming}  does not match the '
                f'expected "{matcher}"'
            )

    def match_optional(self, matcher) -> bool:
        """
        Increments and returns true if matcher matches either the content or
        the type of the upcoming token, otherwise returns false (no increment).
        """

        if self.pos >= self.len:
            return False

        return seq in self.tokens[self.pos]

    def end(self) -> bool:
        return self.pos >= self.len


def parse(reader: Reader) -> Program:
    pass