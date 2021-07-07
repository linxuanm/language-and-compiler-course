class CodeGenContext:
    """
    Referenced and edited during the code generation phrase.

    Contains more concrete information than the semantic analysis pass phrase
    (such as the specific termination location of certain code structures).
    """

    def __init__(self):
        self.scope = []