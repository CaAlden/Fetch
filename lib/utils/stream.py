''' Wrapper stream definitions'''

import abc

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
