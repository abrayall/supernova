import time
import board
import busio
import traceback
import adafruit_icm20649

icm = None
while icm == None:
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        time.sleep(3)
        icm =  adafruit_icm20649.ICM20649(i2c)
    except Exception:
        traceback.print_exc()
        time.sleep(1)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (icm.gyro))
    time.sleep(0.5)
