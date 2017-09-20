''' Create an object that is able to process incoming images.'''

import abc
import cv2
import numpy as np

class ImageProcessor(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, input_stream, output_stream):
        ''' The image processor receives images from the input_stream,
            processes the images, and passes the processed images back out
            of the output stream.'''
        self.input_stream = input_stream
        self.output_stream = output_stream

    @abc.abstractmethod
    def process(self, image):
        pass

    def start(self):
        ''' Run the processor'''
        image = self.input_stream.read()
        self.output_stream.write(self.process(image))

class ProcessAccumulator(ImageProcessor):

    def __init__(self, input_stream, output_stream, process_list):
        super().__init__(input_stream, output_stream)
        self.process_list = process_list

    def process(self, image):
        for proc in self.process_list:
            self.output_stream.write(image)
            image = proc(image)
        return image

def process_circles(image):
    print("About to process circles")
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 300, param1=50, param2=50, minRadius=50, maxRadius=300)
    print("Done!")

    if circles is not None:
        print("Circles found")
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    return image

def process_blur(image):
    return cv2.medianBlur(image, 5)

def process_color(image, colorMode=cv2.COLOR_RGB2GRAY):
    print("Processed Color!")
    return cv2.cvtColor(image, colorMode)

def process_single_color(image):
    ''' Filter out the color in the given threshold'''
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([30,150,50])
    upper = np.array([255,255,180])

    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow('mask', mask)

    return cv2.bitwise_and(image, image, mask=mask)
