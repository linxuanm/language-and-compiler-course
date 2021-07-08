class LexerError(SyntaxError):
    pass


class ParserError(SyntaxError):
    pass


class UndeclaredIdentifierError(SyntaxError):
    pass


class DuplicateDeclarationError(SyntaxError):
    pass