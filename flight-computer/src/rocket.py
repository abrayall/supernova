import os
import sys
import time
import threading
import properties

import busio
import board
import gpiozero
import picamera
import altimeter

import state
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
        self.state = State(self)

        self.launchpad = launchpad.Client(self.info.get('name'))
        self.launchpad.on_pair_handler = lambda launchpad: self.pair(launchpad)
        self.launchpad.on_arm_handler = lambda: self.arm()
        self.launchpad.on_disarm_handler = lambda: self.disarm()
        self.launchpad.connect()

        self.webserver = webserver.WebServer(self).start()
        self.led = gpiozero.LED(10)
        self.led.blink(1, 1, 3)

        print(self.info.get('name') + ' is ready!')
        return

    def pair(self, launchpad):
        self.led.on()
        print('Paired with ' + launchpad['name'])

    def arm(self):
        self.state.set('armed')
        self.altimeter.tare()

        location = datetime.now().strftime('data/%Y-%m-%d/%H-%M-%S')
        threading.Thread(target=lambda: self.camera.record(location)).start()
        threading.Thread(target=lambda: self.record(location)).start()
        self.led.blink(.3, .3)
        print(self.info.get('name') + ' armed and recording...')
        return True

    def record(self, location):
        os.makedirs(location, exist_ok=True)
        file = open(datetime.now().strftime(location + '/data.csv'), 'w+')

        loop = 0
        while self.state.get() == 'armed':
            time = int(round(time.time() * 1000))
            altitude = self.altimeter.altitude()
            this.state.append(time, altitude)

            file.write('%d,%d\n' % (time, altitude))
            loop = loop + 1
            if loop % 10 == 0:
                file.flush()

        file.close()
        return stats

    def disarm(self):
        self.state.set('ready')
        self.camera.stop()
        self.led.off()
        print(self.info.get('name') + ' disarmed.')
        return True


class Camera:
    def __init__(self, rocket):
        self.rocket = rocket
        self.camera = picamera.PiCamera(resolution=(1280, 720), framerate=30)
        #self.camera = picamera.PiCamera(resolution=(1920, 1080), framerate=30)
        self.state = 'initialized'

    def record(self, location):
        os.makedirs(location, exist_ok=True)
        self.camera.annotate_text = datetime.now().strftime(self.rocket.info.get('name') + ' %Y-%m-%d %H:%M:%S.%f')[:-3] + ' ' + str(round(self.rocket.altimeter.altitude())) + ' feet'
        self.camera.start_recording(datetime.now().strftime(location + '/video.h264'))
        self.state = 'recording'

        while self.state == 'recording':
            self.camera.annotate_text = datetime.now().strftime(self.rocket.info.get('name') + ' %Y-%m-%d %H:%M:%S.%f')[:-3] + ' ' + str(round(self.rocket.altimeter.altitude())) + ' feet'
            self.camera.capture(datetime.now().strftime(location + '/image-%H-%M-%S.%f.jpg'), use_video_port=True)
            self.camera.wait_recording(.1)


    def stop(self):
        self.state = 'initialized'
        self.camera.stop_recording()


if __name__ == '__main__':
    rocket = Rocket()
    if len(sys.argv) > 1:
        rocket.arm()
        time.sleep(int(sys.argv[1]))
        rocket.disarm()

    while True:
        time.sleep(10)
