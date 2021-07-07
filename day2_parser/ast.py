from day3_semantic_analysis import ExecutionContext
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


class AST:
    """
    The base class of all abstract syntax tree nodes.
    """

    def analysis_pass(self, context: ExecutionContext):
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


class Assign(Stmt):
    """
    Represents an assignment statement (e.g. 'a = 20').
    """

    def __init__(self, var: str, value: Exp):
        self.var = var
        self.value = value


class Return(Stmt):
    """
    Represents an return statement.
    """

    def __init__(self, value: Exp):
        self.value = value


class Break(Stmt):
    """
    Represents a 'break' statement.
    """
    pass


class Continue(Stmt):
    """
    Represents a 'continue' statement.
    """
    pass


class If(Stmt):
    """
    Represents an if-else statement.

    Let else be an empty list if the 'else' statement is empty.
    """

    def __init__(self, condition: Exp, if_code: [Stmt], else_code: [Stmt]):
        self.condition = condition
        self.if_code = if_code
        self.else_code = else_code


class While(Stmt):
    """
    Represents a while statement.
    """

    def __init__(self, condition: Exp, code: [Stmt]):
        self.condition = condition
        self.code = code


class FuncDecl(Decl):
    """
    Represents a function declaration.
    """

    def __init__(self, func_name: str, params: [str], code: [Stmt]):
        self.func_name = func_name
        self.params = params
        self.code = code


class Program(AST):
    """
    The root node of our AST.
    """

    def __init__(self, declarations: [Decl]):
        self.declarations = declarations