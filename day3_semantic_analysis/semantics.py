from .semantic_context import SemanticContext


def analysis(node):
    """
    Returns nothing if the code is valid; otherwise throws an according error.

    Also prepares the nodes (e.g. populate fields, resolve dependencies) for
    code generation.
    """

    context = SemanticContext()
    node.analysis_pass(context)