class Buffer:
    def __init__(self):
        self.last = None
        self.previous = None

    def append(self, value):
        self.previous = self.last
        self.last = value

if __name__ == '__main__':
    rocket = Rocket()
    if len(sys.argv) > 1:
        rocket.arm()
        time.sleep(int(sys.argv[1]))
        rocket.disarm()

    while True:
        time.sleep(10)
