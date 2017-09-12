''' Create an object that is able to process incoming images.'''

class ImageProcessor():

    def __init__(self, input_stream, output_stream):
        ''' The image processor receives images from the input_stream,
            processes the images, and passes the processed images back out
            of the output stream.'''
        self.input_stream = input_stream
        self.output_stream = output_stream

    def process(self, image):
        ''' Take an image and process it.'''
        pass # TODO: process the image.

    def start(self):
        ''' Run the processor'''
        for image in self.input_stream:
            self.output_stream.write(self.process(image))
