from .context import ExecutionContext


class BaseNode:
    """
    A base tree node.
    """


    def check(self, context: ExecutionContext):
        """
        Checks whether this node contains valid code.
        Performs semantic validation according to the given checking context.

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
        """

        raise NotImplementedError