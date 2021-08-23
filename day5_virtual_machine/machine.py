from .simulation import InteractionHandler, NativeHandler
from .byte_loader import read_bytecode


def run_code(code: [str], io_handler: InteractionHandler = None):

    if io_handler is None:
            io_handler = NativeHandler()

    file_rep = read_bytecode('output.byte')


class VirtualMachine:
    """
    The virtual machine responsible for all code execution.

    Define it however you want.
    """

    def __init__(self, glob_var_count: int, funcs):
        self.glob_vars = [None] * glob_var_count


class Function:
    """
    Represents a function in the code.
    """

    def __init__(self, param_count: int, local_count: int):
        self.param_count = param_count
        self.local_count = local_count