class Buffer:
    def __init__(self):
        self.last = None
        self.previous = None

    def append(self, value):
        self.previous = self.last
        self.last = value
