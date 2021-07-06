import re

from .presets import TokenType, load_source_file


def lex(raw_code: str) -> [(str, TokenType)]:
    pass