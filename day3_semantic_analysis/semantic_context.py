from day1_lexer import DuplicateDeclarationError


# (func_name, params_count)
NATIVE_FUNCS = {
    'print': ['content'],
    'input': ['message'],
    'str_to_int': ['string'],
    'int_to_str': ['int']
}

NATIVE_INDEX = {
    'print': 0,
    'input': 1,
    'str_to_int': 2,
    'int_to_str': 3
}


class Scope:
    """
    A base class that acts as a scope.
    """

    def __init__(self, node=None, counter=0):
        self.vars = {}
        self.counter = counter
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

    def var_index(self, name):
        return self.vars[name]

    def get_node(self):
        return self.node

    def var_count(self):
        return self.counter

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

    def get_func(self, name):
        return self.funcs[name]


class SemanticContext:
    """
    A context object to be used during semantic analysis.

    Its implementation, including its properties and usage, is completely
    up to you.
    """

    pass