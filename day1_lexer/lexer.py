import re
import importlib

from .errors import LexerError
from .presets import TokenType, load_source_file


def lex(raw_code: str) -> [(str, TokenType)]:
    """
    Lexes the given string according to the described syntax.
    Note that this function should automatically strip whitespace tokens.

    return: a list of (token_str, TokenType)

    Example:
        input: "main() {decl a;}"
        output: [
            ('main', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('a', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL)
        ]
    """

    raise NotImplementedError