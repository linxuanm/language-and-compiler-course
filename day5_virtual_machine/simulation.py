class InteractionHandler:
    """
    Used for simulating user inputs and outputs.
    """

    def get_input(self, msg: str) -> str:
        raise NotImplementedError

    def output(self, text: str):
        raise NotImplementedError


class NativeHandler(InteractionHandler):

    def get_input(self, msg: str) -> str:
        return input(msg)

    def output(self, text: str):
        print(text)


class RecordingHandler(InteractionHandler):

    def __init__(self, inputs: [str]):
        self.inputs = inputs
        self.outputs = []
        self.counter = 0

    def get_input(self, msg: str) -> str:
        if self.counter >= len(self.inputs):
            raise RuntimeError('Reached end of input')

        value = self.inputs[self.counter]
        self.counter += 1

        return value

    def output(self, text: str):
        self.outputs.append(text)

    def get_output(self) -> [str]:
        return self.outputs