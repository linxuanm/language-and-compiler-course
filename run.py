import argparse

import day1_lexer as lexer
import day2_parser as parser
import day3_semantic_analysis.semantics as semantics
import day4_code_generation as codegen
import day5_virtual_machine as machine


def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def compile_code(code: str) -> [str]:
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest='action')

    comp_parser = subparsers.add_parser(
        'compile', help='compiles a source file to a bytecode file'
    )
    exec_parser = subparsers.add_parser(
        'exec', help='executes a bytecode file'
    )
    run_parser = subparsers.add_parser(
        'run', help='runs a source file directly'
    )

    comp_parser.add_argument(
        '--source',
        '-s',
        type=str,
        required=True,
        help='the source file to be compiled'
    )
    comp_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default='output.byte',
        help='the path for the output file'
    )

    exec_parser.add_argument(
        '--byte',
        '-b',
        type=str,
        required=True,
        help='the bytecode file to be ran'
    )

    run_parser.add_argument(
        '--source',
        '-s',
        type=str,
        required=True,
        help='the source file to be ran directly'
    )

    args = parser.parse_args()

    if args.action == 'compile':
        code = read_file(args.source)

    elif args.action == 'exec':
        code = read_file(args.byte)

    elif args.action == 'run':
        code = read_file(args.source)