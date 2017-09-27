import picamera
import time

from .stream import Stream

class PiStream(Stream):
    ''' Raspberry Pi Camera Stream'''

    def __init__(self, captureRate, **kwargs):
        self.camera = picamera.PiCamera()
        self.lastCapture = -captureRate
        self.captureRate = captureRate
        for key, arg in kwargs:
            self.camera.__dict__[key] = arg

    def read(self):
        while time.time() - self.lastCapture < self.captureRate:
            time.sleep(0.01)
        capture = self.camera.capture() # TODO: What type of capture
        self.lastCapture = time.time()
        return capture

    def write(self, image):
        raise RuntimeError("Don't write to the RPi Camera")
