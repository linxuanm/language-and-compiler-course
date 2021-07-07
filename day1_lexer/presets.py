import enum


class TokenType(enum.Enum):
    """
    An enum of token types.
    """

    KEYWORD = 'keyword'
    IDENTIFIER = 'identifier'
    LITERAL = 'literal'
    SYMBOL = 'symbol'
    OPERATOR = 'operator'
    WHITESPACE = 'whitespace'

    def __repr__(self):
        return 'TokenType.' + self.name


def load_source_file(path: str) -> str:
    """
    Loads the content of a file as a string (lines separated by line break).
    """

    with open(path, 'r') as f:
        return f.read()