import re
import importlib

from .errors import LexerError
from .presets import TokenType, load_source_file


TOKEN_REGEX = {
    r'(if|else|while|return|break|continue|decl)': TokenType.KEYWORD,
    r'([_a-zA-Z][_a-zA-Z0-9]*)': TokenType.IDENTIFIER,
    r'(NONE|TRUE|FALSE|".*"|\d+)': TokenType.LITERAL,
    r'(,|;|\(|\)|\{|\})': TokenType.SYMBOL,
    r'(==|<=|>=|<|>|=|\+|-|\*|/|&&|\|\|)': TokenType.OPERATOR,
    r'(\s+)': TokenType.WHITESPACE
}

TOKEN_REGEX = {re.compile(k): v for k, v in TOKEN_REGEX.items()}


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

    tokens = []
    while True:

        for k, v in TOKEN_REGEX.items():

            match = re.match(k, raw_code)
            if match is not None:

                content = match.group(0)
                raw_code = raw_code[len(content) :]

                if not v == TokenType.WHITESPACE:
                    tokens.append((content, v))

                break

        else:
            raise LexerError('No tokens found at ' + raw_code)

        if not raw_code:
            return tokens