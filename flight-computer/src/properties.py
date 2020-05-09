
class Properties:
    def __init__(self, properties={}):
        self.properties = properties

    def load(self, file):
        with open(file, 'r') as file:
            for line in file.readlines():
                parts = line.split('=')
                self.set(parts[0].strip(), parts[1].strip())

        return self

    def set(self, name, value):
        self.properties[name] = value

    def get(self, name, default=None):
        return self.properties.get(name, default)

    def all(self):
        return self.properties

