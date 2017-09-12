''' Wrapper stream definitions'''

import abc

class Stream():
    __metaclass__ = abc.ABCMeta()

    @abc.abstractmethod()
    def read():
        ''' Read from the stream'''
        pass

    @abc.abstractmethod()
    def write(data):
        ''' Write data to the Stream'''
        pass

    def __next__(self):
        ''' Get the next element from the stream'''
        yield self.read()

class ImageStream(Stream):
    #TODO: obtain pi resource.

    def read():
        pass # TODO: Parse the image into an open CV style image.

    def write(image):
        raise RuntimeError('Cannot write to an image stream!')

class ImageViewer(Stream):

    def read():
        raise RuntimeError('Cannot read from the image viewer.')

    def write(image):
        pass # TODO: display the image in the viewer.
