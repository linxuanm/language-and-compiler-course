from day1_lexer import (
    UndeclaredIdentifierError,
    MisplacedControlFlowError,
    InvalidParametersError
)
from day3_semantic_analysis.semantic_context import (
    SemanticContext,
    Scope,
    GlobalScope,
    NATIVE_FUNCS,
    NATIVE_INDEX
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
        return 'Declare([%s])'%(', '.join(f"'{i}'" for i in self.vars))

    def __eq__(self, other):
        return type(other) == Declare and \
               compare_unordered(self.vars, other.vars)

    def analysis_pass(self, context: SemanticContext) -> None:
        curr = context.find_closest(lambda _: True)
        for i in self.vars:
            curr.add_var(i)

    def code_length(self) -> int:
        return 0 # declaration is purely compile-time

    def generate_code(self, context: CodeGenContext) -> [str]:
        return []

    def var_count(self) -> int:
        return len(self.vars)


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
        scope = context.find_closest(lambda x, var=self.var: x.has_var(var))
        if scope is None:
            raise UndeclaredIdentifierError(
                f'Variable {self.var} is not declared'
            )

        self.value.analysis_pass(context)
        self.var_info = (
            scope.var_index(self.var),
            isinstance(scope, GlobalScope)
        )

    def code_length(self) -> int:
        return 1 + self.value.code_length()

    def generate_code(self, context: CodeGenContext) -> [str]:
        value_code = self.value.generate_code(context)

        context.increment()
        if self.var_info[1]:
            value_code.append(f'gstore {self.var_info[0]}')
        else:
            value_code.append(f'lstore {self.var_info[0]}')

        return value_code


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
        self.value.analysis_pass(context)

    def code_length(self) -> int:
        return 1 + self.value.code_length()

    def generate_code(self, context: CodeGenContext) -> [str]:
        code = self.value.generate_code(context)

        context.increment()
        return code + ['ret']


class Break(Stmt):
    """
    Represents a 'break' statement.
    """

    def __str__(self):
        return 'Break'

    def __eq__(self, other):
        return type(other) == Break

    def analysis_pass(self, context: SemanticContext) -> None:
        scope = context.find_closest(lambda x: isinstance(x.node, While))

        if scope is None:
            raise MisplacedControlFlowError('Break outside of loop')

        self.outer = scope.get_node()

    def code_length(self) -> int:
        return 1 # just jump

    def generate_code(self, context: CodeGenContext) -> [str]:
        context.increment()

        return [f'jmp {self.loop.get_loop_end() + 1}']


class Continue(Stmt):
    """
    Represents a 'continue' statement.
    """
    def __str__(self):
        return 'Continue'

    def analysis_pass(self, context: SemanticContext) -> None:
        scope = context.find_closest(lambda x: isinstance(x.node, While))

        if scope is None:
            raise MisplacedControlFlowError('Continue outside of loop')

        self.loop = scope

    def code_length(self) -> int:
        return 1 # just jump

    def generate_code(self, context: CodeGenContext) -> [str]:
        context.increment()

        return [f'jmp {self.loop.get_loop_end()}']


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
        self.cond.analysis_pass(context)

        if_scope = Scope(self)
        context.push_scope(if_scope)

        for i in self.if_code:
            i.analysis_pass(context)

        context.pop_scope()

        else_scope = Scope(self)
        context.push_scope(else_scope)

        for i in self.else_code:
            i.analysis_pass(context)

        context.pop_scope()

    def code_length(self) -> int:
        if_len = sum(i.code_length() for i in self.if_code)
        else_len = sum(i.code_length() for i in self.else_code)
        return self.cond.code_length() + if_len + else_len + 2 # 2 jumps

    def generate_code(self, context: CodeGenContext) -> [str]:

        cond_code = self.cond.generate_code(context)

        # initial 'if' branch jump
        context.increment()

        # code length
        if_length = sum(i.code_length() for i in self.if_code)
        else_length = sum(i.code_length() for i in self.else_code)

        # start of 'if' branch
        if_branch_start = context.get_counter() + else_length + 1 # extra 'jmp'
        if_branch_end = if_branch_start + if_length

        else_branch = sum(
            [i.generate_code(context) for i in self.else_code],
            []
        )

        # 'jmp' to end
        context.increment()

        if_branch = sum(
            [i.generate_code(context) for i in self.if_code],
            []
        )

        start_jmp = f'cjmp {if_branch_start}'
        middle_jmp = f'jmp {if_branch_end}'

        return [*cond_code, start_jmp, *else_branch, middle_jmp, *if_branch]


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
        self.cond.analysis_pass(context)

        scope = Scope(self)
        context.push_scope(scope)

        for i in self.code:
            i.analysis_pass(context)

        context.pop_scope()

    def code_length(self) -> int:
        return sum(i.code_length() for i in self.code) + \
               self.cond.code_length() + 2

    def generate_code(self, context: CodeGenContext) -> [str]:

        # for the jumping to conditional branch at bottom
        context.increment()

        # for the structure of a loop
        self.start = context.get_counter()
        self.end = self.start + self.code_length() - 1 # before 'cjmp'

        # generate code
        code = sum([i.generate_code(context) for i in self.code], [])

        # branching location
        context.increment()

        # condition
        cond_code = self.cond.generate_code(context)

        header = f'jmp {self.end}'
        footer = f'cjmp {self.start}'

        return [header, *code, *cond_code, footer]

    # call-backed during code generation by 'continue' and 'break'
    def get_loop_end(self) -> int:
        """
        Returns the instruction position before the looping 'cjmp'.
        """

        return self.end


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

    def register(self, context: SemanticContext) -> None:
        """
        Registers a function to the global scope.

        Neede prior to analysis pass to populate all declaration fields.
        """

        context.glob().add_func(self.func_name, self)

    def analysis_pass(self, context: SemanticContext) -> None:
        scope = Scope(self)

        for i in self.params:
            scope.add_var(i)

        context.push_scope(scope)
        for i in self.code:
            i.analysis_pass(context)

        self.var_count = scope.var_count()
        context.pop_scope()

    def code_length(self) -> int:
        return sum(i.code_length() for i in self.code)

    def generate_code(self, context: CodeGenContext) -> [str]:

        # header and footer do not count toward code length
        header = f'{self.func_name} {len(self.params)} {self.var_count}'
        footer = f':{self.func_name}'

        body = sum([i.generate_code(context) for i in self.code], [])
        body = [' ' * 4 + i for i in body]

        return [header, *body, footer]


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

    def analysis_pass(self, context: SemanticContext):
        global_scope = GlobalScope(self)

        for name, params in NATIVE_FUNCS.items():
            global_scope.add_func(name, FuncDecl(name, params, []))

        context.push_scope(global_scope)

        for i in self.var_decl:
            i.analysis_pass(context)

        for i in self.func_decl:
            i.register(context)

        for i in self.func_decl:
            i.analysis_pass(context)

        context.pop_scope()

    def generate_code(self, context: CodeGenContext) -> [str]:
        code = [
            str(sum(i.var_count() for i in self.var_decl)),
            str(len(self.func_decl)),
        ]

        for i in self.func_decl:
            func_context = CodeGenContext()

            func_code = i.generate_code(func_context)

            # -2 due to function header and footer
            assert len(func_code) - 2 == func_context.get_counter()

            code.append('')
            code += func_code

        return code


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

        context.increment()
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

    def analysis_pass(self, context: SemanticContext):
        self.value.analysis_pass(context)

    def code_length(self):
        return self.value.code_length() + 1

    def generate_code(self, context: CodeGenContext) -> [str]:
        code = self.value.generate_code(context)

        context.increment()
        return code + [UNOP_CODE[self.op]]

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
        pass

    def code_length(self) -> int:
        return 1

    def generate_code(self, context: CodeGenContext) -> [str]:
        context.increment()

        if self.value == 'NONE':
            return ['lnon']
        elif self.value == 'TRUE':
            return ['lboo 1']
        elif self.value == 'FALSE':
            return ['lboo 0']
        elif self.value.isnumeric():
            return [f'lint {self.value}']
        else:
            return [f'lstr {self.value}']


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
        scope = context.find_closest(lambda x, name=self.name: x.has_var(name))
        if scope is None:
            raise UndeclaredIdentifierError(
                f'Variable {self.name} is not declared'
            )

        self.var_info = (
            scope.var_index(self.name),
            isinstance(scope, GlobalScope)
        )

    def code_length(self) -> int:
        return 1

    def generate_code(self, context: CodeGenContext) -> [str]:
        context.increment()

        if self.var_info[1]:
            return [f'gload {self.var_info[0]}']
        else:
            return [f'lload {self.var_info[0]}']


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
        scope = context.glob()
        if not scope.has_func(self.name):
            raise UndeclaredIdentifierError(
                f'Function {self.name} is not declared'
            )

        func = scope.get_func(self.name)
        if len(func.params) != len(self.params):
            raise InvalidParametersError(
                f'Function {self.name} takes {len(func.params)} arguments, '
                f'but was called with {len(self.params)} arguments'
            )

        for i in self.params:
            i.analysis_pass(context)

    def code_length(self) -> int:
        return sum(i.code_length() for i in self.params) + 1

    def generate_code(self, context: CodeGenContext) -> [str]:

        if self.name in NATIVE_INDEX:
            end = f'ncall {NATIVE_INDEX[self.name]}'
        else:
            end = f'call {self.name}'

        params_code = []
        for i in self.params:
            params_code += i.generate_code(context)

        context.increment()
        return params_code + [end]


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
        self.value.analysis_pass(context)

    def code_length(self) -> int:
        return self.value.code_length() + 1

    def generate_code(self, context: CodeGenContext) -> [str]:
        code = self.value.generate_code(context) + ['pop']
        context.increment()
        return code


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