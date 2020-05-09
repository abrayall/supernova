import sys
import time
import threading
import adafruit_bmp3xx

class Altimeter:
    def __init__(self, i2c):
        self.i2c = i2c
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
        self.bmp.filter_coefficient = 8
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2
        self.bmp.sealevel_pressure = 1013.25

    def altitude(self):
        return self.bmp.altitude * 3.28

class Calibrator:
    def __init__(self, altimeter):
        self.altimeter = altimeter
        self.calibrating = False
        self.count = 0
        self.total = 0        

    def start(self):
        self.thread = threading.Thread(target=self.run).start()
        return self

    def run(self):
        self.calibrating = True
        while self.calibrating:
            time.sleep(.5)
            self.count = self.count + 1
            self.total = self.total + self.altimeter.bmp.altitude
  
    def result(self):
        self.calibrating = False
        return self.total / self.count

    def reset(self):
        self.max = 0
        self.min - sys.maxsize
        return self

