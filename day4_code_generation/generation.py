from day2_parser import *


def generate(node: Program) -> [str]:
    """
    Generates the code for a given program.
    """

    return node.generate_code()