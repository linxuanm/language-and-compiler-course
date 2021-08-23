class LexerError(SyntaxError):
    """
    Any error detected during lexical analysis (e.g. unfinished input, no
    matching token rule).
    """
    pass


class ParserError(SyntaxError):
    """
    Any parsing error detected.
    """
    pass


class UndeclaredIdentifierError(SyntaxError):
    """
    When an undeclared variable/function is used.
    """
    pass


class DuplicateDeclarationError(SyntaxError):
    """
    When a variable/function is declared more than once.
    """
    pass


class MisplacedControlFlowError(SyntaxError):
    """
    When a control flow altering statement is misplaced (e.g. 'break' outside
    of a loop).
    """
    pass


class InvalidParametersError(SyntaxError):
    """
    When a function is invoked with the incorrect amount of parameters.
    """
    pass


class InvalidByteSyntaxError(SyntaxError):
    """
    When the syntax of a bytecode file is not valid.
    """
    pass