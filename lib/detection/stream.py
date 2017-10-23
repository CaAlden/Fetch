''' Wrapper stream definitions'''

import abc
import cv2
import numpy as np

class Stream(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read(self):
        ''' Read from the stream'''
        pass

    @abc.abstractmethod
    def write(self, data):
        ''' Write data to the Stream'''
        pass

    def __next__(self):
        ''' Get the next element from the stream'''
        print("called!")
        yield self.read()

    def __iter__(self):
        return self


class ObjectStream(Stream):
    ''' Basic stream that holds a resource, writing updates the resource,
        reading reads the current resource.'''

    def __init__(self, resource):
        self.resource = resource

    def write(self, image):
        self.resource = image

    def read(self):
        return self.resource

class ImageStream(Stream):
    def __init__(self, inputFile):
        self.filename = inputFile

    def read(self):
        return cv2.imread(self.filename)

    def write(self, image):
        raise RuntimeError('Cannot write to an image stream!')

class MultiImageStream(Stream):
    def __init__(self, inputFiles):
        self.infiles = inputFiles

    def read(self):
        if any(self.infiles):
            first = self.infiles[0]
            self.infiles = self.infiles[1:]
            return cv2.imread(first)
        else:
            return None

    def write(self, image):
        raise RuntimeError('Cannot write to an image stream!')


class ImageViewer(Stream):

    def __init__(self, windowName):
        self.windowName = windowName

    def read(self):
        raise RuntimeError('Cannot read from the image viewer.')

    def write(self, image):
        cv2.imshow(self.windowName, image)
        cv2.waitKey(1)
        print("Showing image")

class CircleCenters(Stream):
    def read(self):
        raise RuntimeError("Don't write to out stream")

    def write(self, circles):
        if circles is not None:
            print("Circles found\n\n")
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                print("({}, {}) radius {} px".format(x, y, r))

            print("\n")
