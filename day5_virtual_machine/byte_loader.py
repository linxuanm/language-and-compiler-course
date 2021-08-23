import re

from day1_lexer import InvalidByteSyntaxError


SPLIT_REGEX = re.compile(r'(?:[^\s"]+|"[^"]*")+')


def read_bytecode(path: str):
    """
    Reads a bytecode file. The correctness of bytecode format is assumed;
    nonetheless, throw an InvalidByteSyntaxError if you want.
    """

    out = {}

    with open(path, 'r') as f:
        lines = f.readlines()

    lines = [i.strip() for i in lines if i.strip()]

    out['glob_var_count'] = int(lines[0])
    out['func_count'] = int(lines[1])

    funcs = []
    curr = 2
    for i in range(out['func_count']):
        func_decl = lines[curr]
        curr += 1

        name, param_count, local_count = func_decl.split()
        code = []
        while not lines[curr].startswith(':'):
            code.append(re.findall(SPLIT_REGEX, lines[curr]))
            curr += 1

        curr += 1

        funcs.append({
            'name': name,
            'param_count': param_count,
            'local_count': local_count,
            'code': code
        })

    out['funcs'] = funcs

    return out