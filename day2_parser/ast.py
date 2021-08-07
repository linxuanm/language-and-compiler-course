from day1_lexer import (
    UndeclaredIdentifierError,
    MisplacedControlFlowError,
    InvalidParametersError
)
from day3_semantic_analysis.semantic_context import (
    SemanticContext,
    Scope,
    GlobalScope,
    NATIVE_FUNCS
)
from day4_code_generation import (
    UNOP_CODE,
    BINOP_CODE,
    CodeGenContext
)


class AST:
    """
    The base class of all abstract syntax tree nodes.
    """

    def analysis_pass(self, context: SemanticContext) -> None:
        """
        The analysis pass whether this node contains valid code.
        Performs semantic validation according to the given checking context.

        After the analysis pass, an AST node should have all the information it
        need to generate its bytecode directly.

        Throws an according error if the validation does not pass.
        """

        raise NotImplementedError

    def code_length(self) -> int:
        """
        Returns the length of the generated code of this node (recursive).

        Used for determining the position of jumps prior to the actual
        code generation.
        """

        raise NotImplementedError

    def generate_code(self) -> [str]:
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
        return 'Declare([%s])'%(', '.join(f"'{i}'" for i in self.vars))

    def __eq__(self, other):
        return type(other) == Declare and \
               compare_unordered(self.vars, other.vars)

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class Assign(Stmt):
    """
    Represents an assignment statement (e.g. 'a = 20').
    """

    def __init__(self, var: str, value: Exp):
        self.var = var
        self.value = value

    def __str__(self):
        return f'Assign(\'{self.var}\', {self.value})'

    def __eq__(self, other):
        return type(other) == Assign and \
               self.var == other.var and \
               self.value == other.value

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class Return(Stmt):
    """
    Represents an return statement.
    """

    def __init__(self, value: Exp):
        self.value = value

    def __str__(self):
        return f'Return({self.value})'

    def __eq__(self, other):
        return type(other) == Return and \
               self.value == other.value

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class Break(Stmt):
    """
    Represents a 'break' statement.
    """

    def __str__(self):
        return 'Break'

    def __eq__(self, other):
        return type(other) == Break

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class Continue(Stmt):
    """
    Represents a 'continue' statement.
    """
    def __str__(self):
        return 'Continue'

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


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

        return f'If({self.cond}, {self.if_code}, {self.else_code})'

    def __eq__(self, other):
        return type(other) == If and \
                self.cond == other.cond and \
               self.if_code == other.if_code and \
               self.else_code == other.else_code

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class While(Stmt):
    """
    Represents a while statement.
    """

    def __init__(self, cond: Exp, code: [Stmt]):
        self.cond = cond
        self.code = code

    def __str__(self):
        return f'While({self.cond}, {self.code})'

    def __eq__(self, other):
        return type(other) == While and \
               self.cond == other.cond and \
               self.code == other.code

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class FuncDecl(Decl):
    """
    Represents a function declaration.
    """

    def __init__(self, func_name: str, params: [str], code: [Stmt]):
        self.func_name = func_name
        self.params = params
        self.code = code

    def __str__(self):
        return f'FuncDecl(\'{self.func_name}\', {self.params}, {self.code})'

    def __eq__(self, other):
        return type(other) == FuncDecl and \
               self.func_name == other.func_name and \
               self.params == other.params and \
               self.code == other.code

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class Program(AST):
    """
    The root node of our AST.
    """

    def __init__(self, declarations: [Decl]):
        self.var_decl = [i for i in declarations if isinstance(i, Declare)]
        self.func_decl = [i for i in declarations if isinstance(i, FuncDecl)]

    def __str__(self):
        return f'Program({self.var_decl}, {self.func_decl})'

    def __eq__(self, other):
        return type(other) == Program and \
               compare_unordered(self.var_decl, other.var_decl) and \
               compare_unordered(self.func_decl, other.func_decl)

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


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

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError

        return left_code + right_code + [BINOP_CODE[self.op]]

    def __str__(self):
        return f'{self.op}({self.left}, {self.right})'

    def __eq__(self, other):
        return type(other) == BinOp and \
               self.op == other.op and \
               self.left == other.left and \
               self.right == other.right


class UnOp(Exp):
    """
    Represents an unary operator and its operands. This one is already written
    for you.
    """

    def __init__(self, op: str, value: Exp):
        self.op = op
        self.value = value

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError

    def __str__(self):
        return f'{self.op}({self.value})'

    def __eq__(self, other):
        return type(other) == UnOp and \
               self.op == other.op and \
               self.value == other.value


class Literal(Exp):
    """
    Represents a single literal value.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'Literal(\'{self.value}\')'

    def __eq__(self, other):
        return type(other) == Literal and \
               self.value == other.value

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class VarExp(Exp):
    """
    Represents the evaluation of a variable.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'VarExp(\'{self.name}\')'

    def __eq__(self, other):
        return type(other) == VarExp and \
               self.name == other.name

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class FuncCall(Exp):
    """
    Represents a function invocation.
    """

    def __init__(self, name: str, params: [Exp]):
        self.name = name
        self.params = params

    def __str__(self):
        return f'FuncCall(\'{self.name}\', {self.params})'

    def __eq__(self, other):
        return type(other) == FuncCall and \
               self.name == other.name and \
               self.params == other.params

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


class ExpStmt(Stmt):
    """
    A statement where there is a single discarded expression value.
    """

    def __init__(self, value: Exp):
        self.value = value

    def __str__(self):
        return f'ExpStmt({self.value})'

    def __eq__(self, other):
        return type(other) == ExpStmt and \
               self.value == other.value

    def analysis_pass(self, context: SemanticContext) -> None:
        raise NotImplementedError

    def code_length(self) -> int:
        raise NotImplementedError

    def generate_code(self) -> [str]:
        raise NotImplementedError


def compare_unordered(a, b):
    """
    Compares two lists without considering their order.
    Kinda ugly but AST nodes are not hashable.
    """

    b = list(b)

    try:
        for i in a:
            b.remove(i)
    except ValueError:
        return False

    return True