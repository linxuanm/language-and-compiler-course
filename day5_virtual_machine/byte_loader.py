import re

from day1_lexer import InvalidByteSyntaxError


SPLIT_REGEX = re.compile(r'(?:[^\s"]+|"[^"]*")+')

INT_PARAM = {
    'gload',
    'gstore',
    'lload',
    'lstore',
    'lint',
    'jmp',
    'cjmp',
    'ncall'
}

PREP_FUNCS = {'lboo': lambda b: b == 'TRUE'}

for i in INT_PARAM:
    PREP_FUNCS[i] = lambda line: [line[0], int(line[1])]


def read_bytecode(path: str) -> [[str]]:
    """
    Reads a bytecode file. The correctness of bytecode format is assumed;
    nonetheless, throw an InvalidByteSyntaxError if you want.
    """

    out = {}

    with open(path, 'r') as f:
        lines = f.readlines()

    lines = [i.strip() for i in lines if i.strip()]

    out['glob_var_count'] = int(lines[0])
    func_count = int(lines[1])

    funcs = []
    curr = 2
    for i in range(func_count):
        func_decl = lines[curr]
        curr += 1

        name, param_count, local_count = func_decl.split()
        param_count, local_count = int(param_count), int(local_count)

        code = []
        while not lines[curr].startswith(':'):
            code.append(re.findall(SPLIT_REGEX, lines[curr]))
            curr += 1

        curr += 1

        funcs.append({
            'name': name,
            'param_count': param_count,
            'local_count': local_count,
            'code': preprocess(code)
        })

    out['funcs'] = funcs

    return out


def preprocess(code: [[str]]):
    """
    Preprocesses code into a more manageable form (e.g. convert params
    to int).
    """

    return [PREP_FUNCS[i[0]](i) if i[0] in PREP_FUNCS else i for i in code]