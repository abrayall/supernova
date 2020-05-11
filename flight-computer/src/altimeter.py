import sys
import time
import threading
import adafruit_bmp3xx

class Altimeter:
    # TODO: add auto lookup of pressure via
    # https://forecast.weather.gov/MapClick.php?lat=42.93&lon=-71.44
    def __init__(self, i2c):
        self.i2c = i2c
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
        self.bmp.filter_coefficient = 8
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2
        self.bmp.sealevel_pressure = 1013.25
        self.base = 0

    def altitude(self):
        return (self.base - self.bmp.altitude) * 3.28

    def tare(self):
        count = 0
        total = 0

        for i in range(1, 10):
            time.sleep(.1)
            count = count + 1
            total = total + self.bmp.altitude

        self.base = total / count
        return self
