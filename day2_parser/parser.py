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

        self.pos += 1

    def match_optional(self, matcher) -> bool:
        """
        Increments and returns true if matcher matches either the content or
        the type of the upcoming token, otherwise returns false (no increment).
        """

        if self.pos >= self.len:
            return False

        if seq in self.tokens[self.pos]:
            self.pos += 1
            return true

        return False

    def peek(self) -> (str, TokenType):
        """
        Returns the next token. No increments.
        Raises a ParserError if the token list is fully consumed.

        Should only be used for debugging/printing errors.
        """
        if self.pos >= self.len:
            raise ParserError('End of token sequence')

        return self.tokens[self.pos]

    def end(self) -> bool:
        return self.pos >= self.len


def parse(reader: Reader) -> Program:
    while not reader.end():
        if reader.match_optional('decl'):
            pass
        elif reader.match_optional(TokenType.IDENTIFIER):
            pass
        else:
            raise ParserError(
                f'Unexpected token {reader.peek()} '
                'encountered in the global scope'
            )