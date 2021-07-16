from day1_lexer import DuplicateDeclarationError


class Scope:
    """
    A base class that acts as a scope.
    """

    def __init__(self, node=None):
        self.vars = {}
        self.counter = 0
        self.node = node

    def has_var(self, name):
        return name in self.vars

    def add_var(self, name):
        if name in self.vars:
            raise DuplicateDeclarationError(
                f'Variable {name} declared '
                'multiple times'
            )

        self.vars[name] = self.counter
        self.counter += 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Scope({type(self.node).__name__}, {self.vars})'


class GlobalScope(Scope):
    """
    Global scope act like a normal scope, except that it contains function
    declarations.
    """

    def __init__(self, program):
        super(GlobalScope, self).__init__(program)
        self.funcs = {}

    def has_func(self, name):
        return name in self.funcs

    def add_func(self, name, func):
        if name in self.funcs:
            raise DuplicateDeclarationError(
                f'Function {name} declared '
                'multiple times'
            )

        self.funcs[name] = func


class SemanticContext:
    """
    A context object to be used during semantic analysis.

    Its implementation, including its properties and usage, is completely
    up to you.
    """

    def __init__(self):
        self.scope = []

    def find_closest(self, predicate) -> Scope:
        """
        Retrieves the most recent scope that satisfies the given condition.
        """

        for i in reversed(self.scope):
            if predicate(i):
                return i

    def glob(self) -> GlobalScope:
        """
        Retrieves tne global scope.
        """

        return self.scope[0]

    def push_scope(self, scope: Scope) -> None:
        self.scope.append(scope)

    def pop_scope(self) -> Scope:
        return self.scope.pop()