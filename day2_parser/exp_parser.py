from day1_lexer import TokenType, ParserError

from .ast import *
from .parser import FIRST_SET, Reader


def parse_exp(reader: Reader) -> Exp:
    pass