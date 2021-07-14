from day1_lexer import DuplicateDeclarationError


class Scope:
    """
    A base class that acts as a scope.
    """

    def __init__(self, meta=(None, '')):
        """
        meta is used as a hacky way to store information about the
        corresponding AST node. Its first element corresponds to the actual
        node, while the second element stores extra information (e.g. if/else
        since there is no distinction between the two on a node level).
        """

        self.vars = set()
        self.meta = meta

    def has_var(self, name):
        return name in self.vars

    def add_var(self, name):
        if name in self.vars:
            raise DuplicateDeclarationError(
                f'Variable {name} declared '
                'multiple times'
            )

        self.vars.add(name)


class GlobalScope(Scope):
    """
    Global scope act like a normal scope, except that it contains function
    declarations.
    """

    def __init__(self, meta=(None, '')):
        super(GlobalScope, self).__init__(meta)
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