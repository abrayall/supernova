import numpy
import numpy_ringbuffer

class Buffer(numpy_ringbuffer.RingBuffer):
    def __init__(self, capacity, data_type=numpy.int, allow_overwrite=True):
        self.last = None
        super().__init__(capacity, data_type, allow_overwrite)

    def append(self, value):
        self.last = value
        super().append(value)

if __name__ == '__main__':
    rocket = Rocket()
    if len(sys.argv) > 1:
        rocket.arm()
        time.sleep(int(sys.argv[1]))
        rocket.disarm()

    while True:
        time.sleep(10)
