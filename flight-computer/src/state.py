import buffer
import numpy

class State:
    def __init__(self, rocket):
        self.state = 'ready'
        self.timestamps = buffer.Buffer(100, numpy.int)
        self.altitudes = buffer.Buffer(100, numpy.int)
        self.events = {}

    def set(self, state):
        self.state = state

    def get(self):
        return self.state

    def append(self, timestamp, altitude):
        if (self.altitudes.last != None):
            self.analyze(timestamp, altitude)

        self.timestamps.append(timestamp)
        self.altitudes.append(altitude)

    def analyze(self, timestamp, altitude):
        difference = self.difference(self.altitudes.last, altitude)
        duration = self.duration(self.timestamps.last, timestamp)
        rate = (difference / duration) * 1000
        #print('     ', rate, difference, duration)
        if (self.state == 'armed' and difference > 1):
            print('launch detected', self.altitudes.last)
            self.events['launch'] = (self.timestamps.last, self.altitudes.last)
            self.state = 'launched'
        elif (self.state == 'launched' and difference <= 0):
            print('apogee detected at', max(altitude, self.altitudes.last))
            self.state = 'apogee'
            self.events['apogee'] = (timestamp, max(altitude, self.altitudes.last))
            if (difference < 0):
                print('decent detected')
                self.state = 'desending'
                self.events['descent'] = (timestamp, altitude)
        elif (self.state == 'apogee' and difference < 0):
            print('decent detected')
            self.state = 'desending'
            self.events['descent'] = (timestamp, altitude)
        elif (self.state == 'desending' and difference == 0):
            print('landing detected', altitude)
            self.state = 'landed'
            self.events['landing'] = (timestamp, altitude)
        elif (self.state == 'landed' and timestamp - self.events['landing'][0] > 5000):
            print('complete')
            self.state = 'complete'

    def rate(self):
        return differce

    def difference(self, start, end):
        return end - start

    def duration(self, start, end):
        return end - start
