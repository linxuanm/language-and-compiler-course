from .simulation import InteractionHandler, NativeHandler


def run_code(code: [str], io_handler: InteractionHandler = None):

    if io_handler is None:
            io_handler = NativeHandler()

    pass