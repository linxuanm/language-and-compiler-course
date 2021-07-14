class SemanticContext:
    """
    A context object to be used during semantic analysis.

    Its implementation, including its properties and usage, is completely
    up to you.
    """

    def __init__(self):
        self.scope = []

    def find_closest(self, clazz):
        """
        Retrieves the most recent scope that satisfies the class condition.
        """

        for i in reversed(self.scope):
            if isinstance(i, clazz):
                return i