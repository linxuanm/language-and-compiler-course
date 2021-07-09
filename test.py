# THIS FILE IS FOR TESTING YOUR CODE; DO NOT EDIT ITS CONTENT
#
# The testing of each step in the compilation process returns
# the processed content in the form of a list for simplicity.

import os
import sys
import functools

import day1_lexer as lexer
import day2_parser as parser
import day3_semantic_analysis as semantic
import day4_code_generation as codegen
import day5_virtual_machine as machine

from day2_parser.ast import *

TokenType = lexer.TokenType


CODE_DIR = 'test_code'
CODE_FILES = {
    'global_decl.code': {
        'tokens': [
            ('decl', TokenType.KEYWORD),
            ('a', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b_variable', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('c', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('d', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('e', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('f', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('ashduiahsgjdha', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('sjbdjshdbf', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('ASgdjhashjJAJHHKAS128731_', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('mcn', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('hndf', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('ajksdkfhsdjk', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('A', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('B', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('C', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('D', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('E', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('F', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('G', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL)
        ],
        'ast': Program([
            Declare([
                'a', 'b_variable', 'c', 'd', 'e', 'f', 'ashduiahsgjdha',
                'sjbdjshdbf', 'ASgdjhashjJAJHHKAS128731_'
            ]),
            Declare(['mcn']),
            Declare(['hndf']),
            Declare(['ajksdkfhsdjk']),
            Declare(['A', 'B', 'C', 'D', 'E', 'F', 'G'])])
    },
    'fibonacci.code': {
        'tokens': [
            ('main', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('a', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('0', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('1', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('while', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('<', TokenType.OPERATOR),
            ('1000', TokenType.LITERAL),
            ('&&', TokenType.OPERATOR),
            ('(', TokenType.SYMBOL),
            ('True', TokenType.IDENTIFIER),
            ('||', TokenType.OPERATOR),
            ('True', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('&&', TokenType.OPERATOR),
            ('True', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('a', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('a', TokenType.IDENTIFIER),
            ('-', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('a', TokenType.IDENTIFIER),
            ('-', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('a', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('0', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('"DONE"', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL)
        ],
        'ast': None
    }
}


def get_file_values(all_files, key):
    return {k: v[key] for k, v in all_files.items()}


def supports_color():
    supported = sys.platform != 'Pocket PC' and \
        (sys.platform != 'win32' or 'ANSICON' in os.environ)

    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported and is_a_tty


def log_func(code):
    return (lambda x: print(f'\033[{code}m{x}\033[0m')) \
        if supports_color() else print


good = log_func('32')
bad = log_func('91')
bold = log_func('1')
failure = log_func('1;91')


def abort():
    print()
    failure('TEST FAILED')
    sys.exit(1)


def assert_equal(output, expected, meta=''):
    if output == expected:
        good(f'Test Passed: {meta}')
    else:
        bad('Test Failed:\n')
        bad(f'Expected {expected}\n')
        bad(f'Instead got {output}\n')


def wrap_title(test_name):

    def outer(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            bold(f'Testing {test_name}\n')
            func(*args, **kwargs)
            print()

        return inner

    return outer


@wrap_title('Lexer')
def test_lexer(file_ref):
    ref_tokens = get_file_values(file_ref, 'tokens')
    code_sources = {
        i: lexer.load_source_file(os.path.join(CODE_DIR, i)) for i in file_ref
    }
    tokens = {k: lexer.lex(v) for k, v in code_sources.items()}

    for i in tokens:
        assert_equal(tokens[i], ref_tokens[i], i)


@wrap_title('Parser')
def test_parser(file_ref):
    ref_asts = get_file_values(file_ref, 'ast')
    tokens = get_file_values(file_ref, 'tokens')
    asts = {k: parser.parse(parser.Reader(v)) for k, v in tokens.items()}

    for i in asts:
        assert_equal(asts[i], ref_asts[i], i)


test_lexer(CODE_FILES)
test_parser(CODE_FILES)

good('ALL TEST PASSED')