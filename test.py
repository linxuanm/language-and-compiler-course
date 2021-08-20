# THIS FILE IS FOR TESTING YOUR CODE; DO NOT EDIT ITS CONTENT
#
# The testing of each step in the compilation process returns
# the processed content in the form of a list for simplicity.

import os
import sys
import functools

import day1_lexer as lexer
import day2_parser as parser
import day3_semantic_analysis as semantics
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
    'structures.code': {
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
            ('20', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('0', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('if', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('10', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('add', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('foo', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('casda', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('while', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('TRUE', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('if', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('return', TokenType.KEYWORD),
            ('FALSE', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('add', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('a', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('return', TokenType.KEYWORD),
            ('0', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL)
        ],
        'ast': Program([
            FuncDecl('main', [], [
                Declare(['a', 'b']),
                Assign('a', Literal('20')),
                Assign('b', Literal('0')),
                If(VarExp('a'), [
                    ExpStmt(FuncCall('print', [VarExp('a')]))
                ], []),
                Assign('a', Literal('10')),
                Assign('b', FuncCall('add', [VarExp('a'), VarExp('b')]))
            ]),
            FuncDecl('foo', ['a', 'b', 'casda'], [
                While(Literal('TRUE'), [
                    ExpStmt(FuncCall('print', [VarExp('b')])),
                    If(VarExp('a'), [Return(Literal('FALSE'))], [])
                ])
            ]),
            FuncDecl('add', ['a', 'b'], [Return(Literal('0'))])])
    },
    'fibonacci.code': {
        'tokens': [
            ('main', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('whilea', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('whilea', TokenType.IDENTIFIER),
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
            ('TRUE', TokenType.LITERAL),
            ('||', TokenType.OPERATOR),
            ('FALSE', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            ('&&', TokenType.OPERATOR),
            ('TRUE', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('whilea', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('whilea', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('whilea', TokenType.IDENTIFIER),
            ('-', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('whilea', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('whilea', TokenType.IDENTIFIER),
            ('-', TokenType.OPERATOR),
            ('b', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('b', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('whilea', TokenType.IDENTIFIER),
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
        'ast': Program([
            FuncDecl('main', [], [
                Declare(['whilea', 'b']),
                Assign('whilea', Literal('0')),
                Assign('b', Literal('1')),
                While(
                    BinOp('&&',
                        BinOp('&&',
                            BinOp('<', VarExp('b'), Literal('1000')),
                            BinOp('||', Literal('TRUE'), Literal('FALSE'))
                        ),
                        Literal('TRUE')
                    ),
                    [
                        Assign(
                            'whilea', BinOp('+', VarExp('whilea'), VarExp('b'))
                        ),
                        Assign('b', BinOp('-', VarExp('whilea'), VarExp('b'))),
                        Assign(
                            'whilea', BinOp('-', VarExp('whilea'), VarExp('b'))
                        ),
                        Assign('b', BinOp('+', VarExp('whilea'), VarExp('b'))),
                        ExpStmt(FuncCall('print', [
                            BinOp('+', VarExp('b'), Literal('0'))
                        ]))
                    ]
                ),
                ExpStmt(FuncCall('print', [Literal('"DONE"')]))
            ])
        ])
    },
    'pyramid.code': {
        'tokens': [
            ('decl', TokenType.KEYWORD),
            ('length', TokenType.IDENTIFIER),
            (',', TokenType.SYMBOL),
            ('Counter', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('main', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('length', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('input', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('"Enter length: "', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('pyramid', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('length', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('pyramid', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('length', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('decl', TokenType.KEYWORD),
            ('out_str', TokenType.IDENTIFIER),
            (';', TokenType.SYMBOL),
            ('Counter', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('1', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('out_str', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('"*"', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('while', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('Counter', TokenType.IDENTIFIER),
            ('<=', TokenType.OPERATOR),
            ('length', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('out_str', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('"\\n"', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('out_str', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('out_str', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('"*"', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('Counter', TokenType.IDENTIFIER),
            ('=', TokenType.OPERATOR),
            ('Counter', TokenType.IDENTIFIER),
            ('+', TokenType.OPERATOR),
            ('1', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('return', TokenType.KEYWORD),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL)
        ],
        'ast': Program([
            Declare(['length', 'Counter']),
            FuncDecl('main', [], [
                Assign('length', FuncCall('input', [
                    Literal('"Enter length: "')
                ])),
                ExpStmt(FuncCall('pyramid', [VarExp('length')]))
            ]),
            FuncDecl('pyramid', ['length'], [
                Declare(['out_str']),
                Assign('Counter', Literal('1')),
                Assign('out_str', Literal('"*"')),
                While(BinOp('<=', VarExp('Counter'), VarExp('length')), [
                    ExpStmt(FuncCall('print', [
                        BinOp('+', VarExp('out_str'), Literal('"\\n"'))
                    ])),
                    Assign('out_str', BinOp('+',
                        VarExp('out_str'),
                        Literal('"*"')
                    )),
                    Assign('Counter', BinOp('+',
                        VarExp('Counter'),
                        Literal('1')
                    ))
                ]),
                Return(Literal('NONE'))
            ])
        ])
    },
    'factorial.code': {
        'tokens': [
            ('main', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('print', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('factorio', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('str_to_int', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('input', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('"Get a number: "', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('factorio', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('x', TokenType.IDENTIFIER),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('if', TokenType.KEYWORD),
            ('(', TokenType.SYMBOL),
            ('!', TokenType.OPERATOR),
            ('(', TokenType.SYMBOL),
            ('!', TokenType.OPERATOR),
            ('(', TokenType.SYMBOL),
            ('x', TokenType.IDENTIFIER),
            ('<=', TokenType.OPERATOR),
            ('1', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            (')', TokenType.SYMBOL),
            ('{', TokenType.SYMBOL),
            ('return', TokenType.KEYWORD),
            ('1', TokenType.LITERAL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL),
            ('return', TokenType.KEYWORD),
            ('x', TokenType.IDENTIFIER),
            ('*', TokenType.OPERATOR),
            ('factorio', TokenType.IDENTIFIER),
            ('(', TokenType.SYMBOL),
            ('x', TokenType.IDENTIFIER),
            ('-', TokenType.OPERATOR),
            ('1', TokenType.LITERAL),
            (')', TokenType.SYMBOL),
            (';', TokenType.SYMBOL),
            ('}', TokenType.SYMBOL)
        ],
        'ast': Program([
            FuncDecl('main', [], [
                ExpStmt(FuncCall('print', [
                    FuncCall('factorio', [
                        FuncCall('str_to_int', [
                            FuncCall('input', [Literal('"Get a number: "')])
                        ])
                    ])
                ]))
            ]),
            FuncDecl('factorio', ['x'], [
                If(UnOp('!', UnOp('!',
                    BinOp('<=', VarExp('x'), Literal('1')))), [
                        Return(Literal('1'))
                    ],
                    []
                ),
                Return(BinOp('*',
                    VarExp('x'),
                    FuncCall('factorio', [
                        BinOp('-', VarExp('x'), Literal('1'))
                    ])
                ))
            ])
        ])
    }

}
COMPILE_ERROR_FILES = {
    'error_dup_decl_func.code': lexer.DuplicateDeclarationError,
    'error_dup_decl_simple.code': lexer.DuplicateDeclarationError,
    'error_dup_decl_stmt.code': lexer.DuplicateDeclarationError,
    'error_dup_decl_native.code': lexer.DuplicateDeclarationError,
    'error_undec_similar.code': lexer.UndeclaredIdentifierError,
    'error_undec_simple.code': lexer.UndeclaredIdentifierError,
    'error_undec_complex.code': lexer.UndeclaredIdentifierError,
    'error_undec_return.code': lexer.UndeclaredIdentifierError,
    'error_undec_func.code': lexer.UndeclaredIdentifierError,
    'error_misplaced_control_simple.code': lexer.MisplacedControlFlowError,
    'error_misplaced_control_complex.code': lexer.MisplacedControlFlowError,
    'error_invalid_param_simple.code': lexer.InvalidParametersError,
    'error_invalid_param_complex.code': lexer.InvalidParametersError,
    'error_invalid_param_native.code': lexer.InvalidParametersError
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
        bad(f'Test Failed: {meta}\n')
        bad(f'Expected {expected}\n')
        bad(f'Instead got {output}\n')

        abort()


def expect_error(runnable, error, meta=''):
    try:
        runnable()
    except error:
        good(f'Test Passed: {meta}')
    else:
        bad(f'Test Failed: {meta}')
        bad(f'Expected error: {error.__name__}\n')

        abort()


def wrap_title(test_name):

    def outer(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            bold(f'Testing {test_name}\n')
            value = func(*args, **kwargs)
            print()
            return value

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

    return tokens


@wrap_title('Parser')
def test_parser(file_ref, prev_tokens):
    ref_asts = get_file_values(file_ref, 'ast')
    asts = {}

    # removed dict comprehension to ensure the display of previous results
    # when an unexpected error occurs
    for k, v in prev_tokens.items():
        node = parser.parse(parser.Reader(v))
        assert_equal(node, ref_asts[k], k)
        asts[k] = node

    return asts


@wrap_title('Semantic Analysis')
def test_analysis(asts):
    for i in asts:
        semantics.analysis(asts[i])
        good(f'Test Passed: {i}')


@wrap_title('Code Generation')
def test_generation(asts):
    out_code = {}

    for k, v in asts.items():
        out_code[k] = codegen.generate(v)
        good(f'Test Passed: {k}')

    return out_code


def full_compile(path):
    code = lexer.load_source_file(os.path.join(CODE_DIR, path))
    tokens = lexer.lex(code)
    ast = parser.parse(parser.Reader(tokens))
    semantics.analysis(ast)


@wrap_title('Compile Error Check')
def test_fail(files):
    for i in files:
        expect_error(lambda i=i: full_compile(i), files[i], i)


tokens = test_lexer(CODE_FILES)
asts = test_parser(CODE_FILES, tokens)
test_analysis(asts)
test_fail(COMPILE_ERROR_FILES)
generated = test_generation(asts)

good('ALL TEST PASSED')