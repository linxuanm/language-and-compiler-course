import enum


class TokenType(enum.Enum):

    KEYWORD = 'keyword'
    IDENTIFIER = 'identifier'
    LITERAL = 'literal'
    SYMBOL = 'symbol'
    OPERATOR = 'operator'
    WHITESPACE = 'whitespace'


def load_source_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()