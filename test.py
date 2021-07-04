# THIS FILE IS FOR TESTING YOUR CODE; DO NOT EDIT ITS CONTENT

import os
import sys

import basics
import autograd
import interpreter


exit_code = 0


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


if exit_code == 0:
    good('ALL TEST PASSED')
else:
    failure('TEST FAILED')
    sys.exit(1)