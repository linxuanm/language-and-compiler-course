# THIS FILE IS FOR TESTING YOUR CODE; DO NOT EDIT ITS CONTENT
#
# The testing of each step in the compilation process returns
# the processed content in the form of a list for simplicity.

import os
import sys

lexer = __import__('1-lexer')
parser = __import__('2-parser')
semantic = __import__('3-semantic-analysis')
codegen = __import__('4-code-generation')
machine = __import__('5-virtual-machine')


exit_code = 0

CODE_DIR = 'test_code'
CODE_FILES = {
    'global_decl.code': {
        'tokens': [

        ]
    }
}


def get_file_value(all_files, key):
    pass


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
    global exit_code
    exit_code = 1


def assert_equal(output, expected, meta=''):
    if output == expected:
        good(f'Test Passed{meta}: {output}')
    else:
        bad(f'Test Failed{meta}: Expected {expected}, instead got {output}')
        abort()


def test_lexer(files, expected):
    real_path = [os.path.join(CODE_DIR, i) for i in files]
    code_sources = [lexer.load_source_file(i) for i in files]
    tokens = [lexer.lex(i) for i in code_sources]


#tokens = test_lexer()

if exit_code == 0:
    good('ALL TEST PASSED')
else:
    failure('TEST FAILED')
    sys.exit(1)