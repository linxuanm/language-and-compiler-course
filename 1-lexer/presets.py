import enum


class TokenType(enum.Enum):

    KEYWORD = 'keyword'
    IDENTIFIER = 'identifier'
    LITERAL = 'literal'
    SYMBOL = 'symbol'
    OPERATOR = 'operator'
