from .simulation import InteractionHandler, NativeHandler
from .byte_loader import read_bytecode


def run_code(code: [str], io_handler: InteractionHandler = None):
    """
    Runs a given bytecode.

    Note that all IO actions must be performed with 'io_handler' to
    pass the tests.
    """

    if io_handler is None:
            io_handler = NativeHandler()

    file_rep = read_bytecode('output.byte')
    funcs = {
        i['name']: Function(i['param_count'], i['local_count'], i['code'])
        for i in file_rep['funcs']
    }

    vm = VirtualMachine(io_handler, file_rep['glob_var_count'], funcs)
    vm.run()


class Function:
    """
    Represents a function in the code.
    """

    def __init__(self, param_count: int, local_count: int, code):
        self.param_count = param_count
        self.local_count = local_count
        self.code = code

    def get_code(self, pc: int):
        """
        Gets the code at the given program-counter index.
        """

        return self.code[pc]

    def get_param_count(self):
        return self.param_count

    def get_local_count(self):
        return self.local_count


class Frame:
    """
    Represents a function frame.
    """

    def __init__(self, func: int):
        self.func = func
        self.locals = [None] * self.func.get_local_count()
        self.pc = 0

    def get_local(self, index: int):
        return self.locals[index]

    def set_local(self, index: int, value):
        self.locals[index] = value


class VirtualMachine:
    """
    The virtual machine responsible for all code execution.

    Implement it however you like.
    """

    def __init__(self, io: InteractionHandler, glob_var_count: int, funcs):
        self.glob_vars = [None] * glob_var_count
        self.funcs = funcs
        self.io = io
        self.frame_stack = []
        self.exec_stack = []

    def get_curr_frame(self):
        return self.frame_stack[-1]

    def run(self):
        """
        Executes the 'main' function.
        """

        if not 'main' in self.funcs:
            return

        self.prep_func(self.funcs['main'])

        while self.frame_stack:
            self.execute()

    def prep_func(self, func: Function):
        """
        Prepares to run a function.
        """

        curr_frame = Frame(func)
        self.frame_stack.append(curr_frame)

        # load params
        params = func.get_local_count()
        for i in range(params):
            self.lstore(params - i - 1) # reverse stack order

    def execute(self):
        """
        Runs the code that the program counter is pointing to.
        Responsible for incrementing the program counter.
        """

        pass

    def lload(self, index: int):
        self.exec_stack.append(self.get_curr_frame().get_local(index))

    def lstore(self, index: int):
        self.get_curr_frame().set_local(index, self.exec_stack.pop())