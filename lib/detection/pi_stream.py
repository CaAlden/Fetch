try:
    import picamera
except ImportError:
    print("Warning: Picamera not found")
import cv2
import time

from .stream import Stream

class PiStream(Stream):
    ''' Raspberry Pi Camera Stream'''

    def __init__(self, captureRate, **kwargs):
        self.camera = picamera.PiCamera()
        self.lastCapture = -captureRate
        self.captureRate = captureRate
        for key, arg in kwargs.items():
            setattr(self.camera, key, arg)

    def read(self):
        while time.time() - self.lastCapture < self.captureRate:
            print("Waiting for capture")
            time.sleep(0.01)
        print("Capturing...")
        self.camera.capture('/tmp/temp_capture.png')
        self.lastCapture = time.time()
        return cv2.imread('/tmp/temp_capture.png')

    def write(self, image):
        raise RuntimeError("Don't write to the RPi Camera")
