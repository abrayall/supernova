import os
import time
import threading
import properties

import busio
import board
import picamera
import altimeter

import webserver
import launchpad
from datetime import datetime

class Rocket:
    def __init__(self):
        self.info = properties.Properties().load('rocket.properties')
        print(self.info.get('name') + ' is starting...')

        self.camera = Camera(self)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.altimeter = altimeter.Altimeter(self.i2c)
        self.accelerometer = None

        self.launchpad = launchpad.Client(self.info.get('name'))
        self.launchpad.on_pair_handler = lambda launchpad: self.pair(launchpad)
        self.launchpad.on_arm_handler = lambda: self.arm()
        self.launchpad.on_disarm_handler = lambda: self.disarm()
        self.launchpad.connect()

        self.webserver = webserver.WebServer(self).start()
        self.state = 'ready'

        print(self.info.get('name') + ' is ready!')
        return

    def pair(self, launchpad):
        print('Paired with ' + launchpad['name'])

    def arm(self):
        self.state = 'armed'
        threading.Thread(target=self.camera.record).start()
        threading.Thread(target=self.record).start()
        print('Rocket armed and recording...')
        return True

    def record(self):
        file = open(datetime.now().strftime('data/%Y-%m-%d/%Y-%m-%d_%H-%M-%S.data'), 'w+')
        loop = 0
        while self.state == 'armed':
            file.write('%d,%d\n' % (int(round(time.time() * 1000)), self.altimeter.altitude()))
            loop = loop + 1
            if loop % 10 == 0:
                file.flush()

            #time.sleep(.1)

        file.close()

    def disarm(self):
        self.state = 'ready'
        self.camera.stop()
        print('Rocket disarmed.')
        return True

class Camera:
    def __init__(self, rocket):
        self.rocket = rocket
        self.camera = picamera.PiCamera(resolution=(1920, 1080), framerate=30)
        self.state = 'initialized'

    def record(self):
        os.makedirs(datetime.now().strftime('data/%Y-%m-%d'), exist_ok=True)
        self.camera.annotate_text = datetime.now().strftime(self.rocket.info.get('name') + ' %Y-%m-%d %H:%M:%S.%f')[:-3] + ' ' + str(round(self.rocket.altimeter.altitude())) + ' feet'
        self.camera.start_recording(datetime.now().strftime('data/%Y-%m-%d/%Y-%m-%d_%H-%M-%S.h264'))
        self.state = 'recording'

        while self.state == 'recording':
            self.camera.annotate_text = datetime.now().strftime(self.rocket.info.get('name') + ' %Y-%m-%d %H:%M:%S.%f')[:-3] + ' ' + str(round(self.rocket.altimeter.altitude())) + ' feet'
            self.camera.wait_recording(.3)
            self.camera.capture(datetime.now().strftime('data/%Y-%m-%d/%Y-%m-%d_%H-%M-%S.jpg'), use_video_port=True)

    def stop(self):
        self.state = 'initialized'
        self.camera.stop_recording()

    def picture(self):
        return None

if __name__ == '__main__':
    rocket = Rocket()

    while True:
        time.sleep(10)
