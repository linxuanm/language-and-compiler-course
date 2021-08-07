class CodeGenContext:

    def __init__(self):
        self.counter = 0

    def get_counter(self):
        return self.counter

    def increment(self, amount: int = 1):
        self.counter += amount