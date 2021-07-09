from day3_semantic_analysis import SemanticContext
from day4_code_generation import CodeGenContext


__all__ = [
    'Exp',
    'Declare',
    'Assign',
    'Return',
    'Break',
    'Continue',
    'If',
    'While',
    'FuncDecl',
    'Program'
]


BINOP_CODE = {
    '==': 'equal',
    '!=': 'nequal',
    '<': 'less',
    '>': 'great',
    '<=': 'leq',
    '>=': 'geq',
    '+': 'add',
    '-': 'subtract',
    '*': 'mul',
    '/': 'div'
}

UNOP_CODE = {
    '-': 'neg',
    '!': 'not'
}


class AST:
    """
    The base class of all abstract syntax tree nodes.
    """

    def analysis_pass(self, context: SemanticContext):
        """
        The analysis pass whether this node contains valid code.
        Performs semantic validation according to the given checking context.

        Other analytic operations, such as optimization, are also executed
        here.

        Throws an according error if the validation does not pass.
        """

        raise NotImplementedError

    def code_length(self):
        """
        Returns the length of the generated code of this node (recursive).

        Used for determining the position of jumps prior to the actual
        code generation.
        """

        raise NotImplementedError

    def generate_code(self, context: CodeGenContext) -> [str]:
        """
        Generates the code for this node according to the surronding context.
        Returns the list of bytecode for this node.

        In the case of Exp, generate the necessary code that is needed to
        have the resulting value on top of the stack.
        """

        raise NotImplementedError

    def __repr__(self):
        # for debugging purposes
        return str(self)


class Exp(AST):
    """
    Represents an expression.
    """
    pass


class Stmt(AST):
    """
    An interface for all statement-related nodes.
    """
    pass


class Decl(AST):
    """
    An interface for all global-scope declaration-related nodes.
    """
    pass


class Declare(Stmt, Decl):
    """
    Represents a declare statement (e.g. 'decl a, b;').
    """

    def __init__(self, vars: [str]):
        self.vars = vars

    def __str__(self):
        return 'Declare([%s])'%(', '.join(self.vars))


class Assign(Stmt):
    """
    Represents an assignment statement (e.g. 'a = 20').
    """

    def __init__(self, var: str, value: Exp):
        self.var = var
        self.value = value

    def __str__(self):
        return f'Assign({self.var}, {self.value})'


class Return(Stmt):
    """
    Represents an return statement.
    """

    def __init__(self, value: Exp):
        self.value = value

    def __str__(self):
        return f'Return({self.value})'


class Break(Stmt):
    """
    Represents a 'break' statement.
    """

    def __str__(self):
        return 'Break'


class Continue(Stmt):
    """
    Represents a 'continue' statement.
    """
    def __str__(self):
        return 'Continue'


class If(Stmt):
    """
    Represents an if-else statement.

    Let else be an empty list if the 'else' statement is empty.
    """

    def __init__(self, cond: Exp, if_code: [Stmt], else_code: [Stmt]):
        self.cond = cond
        self.if_code = if_code
        self.else_code = else_code

    def __str__(self):
        if self.else_code:
            return f'IfElse({self.cond}, {self.if_code}, {self.else_code})'

        return f'If({self.cond}, {self.if_code})'


class While(Stmt):
    """
    Represents a while statement.
    """

    def __init__(self, cond: Exp, code: [Stmt]):
        self.cond = cond
        self.code = code

    def __str__(self):
        return f'While({self.cond}, {self.code})'


class FuncDecl(Decl):
    """
    Represents a function declaration.
    """

    def __init__(self, func_name: str, params: [str], code: [Stmt]):
        self.func_name = func_name
        self.params = params
        self.code = code

    def __str__(self):
        return f'FuncDecl("{self.func_name}", {self.params}, {self.code})'


class Program(AST):
    """
    The root node of our AST.
    """

    def __init__(self, declarations: [Decl]):
        self.declarations = declarations

    def __str__(self):
        return f'Program({self.declarations})'


class BinOp(Exp):
    """
    Represents a binary operator and its operands. This one is already written
    for you.

    TECHNICALLY you should use a separate subclass for each operator,
    as that improves the flexibility of the code and conforms to OOP
    standards, but since there is a bijective mapping between the binary
    operators and their bytecode (all of which has length 1), the pattern can
    be abused.
    """

    def __init__(self, op: str, left: Exp, right: Exp):
        self.op = op
        self.left = left
        self.right = right

    def analysis_pass(self, context: SemanticContext):
        # BinOp imposes no addition contextual contraint or information
        self.left.analysis_pass(context)
        self.right.analysis_pass(context)

    def code_length(self):
        return self.left.code_length() + self.right.code_length() + 1

    def generate_code(self, context: CodeGenContext) -> [str]:
        left_code = self.left.generate_code(context)
        right_code = self.right.generate_code(context)

        return left_code + right_code + [BINOP_CODE[self.op]]

    def __str__(self):
        return f'{self.op}({self.left}, {self.right})'


class UnOp(Exp):
    """
    Represents an unary operator and its operands. This one is already written
    for you.
    """

    def __init__(self, op: str, value: Exp):
        self.op = op
        self.value = value

    def analysis_pass(self, context: SemanticContext):
        self.value.analysis_pass(context)

    def code_length(self):
        return self.value.code_length() + 1

    def generate_code(self, context: CodeGenContext):
        return self.value.generate_code(context) + [UNOP_CODE[self.op]]

    def __str__(self):
        return f'{self.op}({self.value})'