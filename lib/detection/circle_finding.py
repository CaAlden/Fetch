''' Functions for finding circles in images.'''

# TODO: OpenCV imports.

def find_circles(image):
    ''' Find circles in the given image file.
        Args:
            image - An image to search through
        Returns:
            List of Circles'''

def dist_from_circle(circle, actual_size, foc_len):
    ''' Given a circle and the known radius of that circle,
        find the distance above the circle.
        Args:
            circle - The circle object to use as a reference
            actual_size - the actual size of the circle in the same units as the foc_len
            foc_len - The focal length of the camera in the same units as the actual_size
        Returns:
            the distance the camera is from the object in units of the foc_len/actual_size'''
    return (foc_len * actual_size) / circle.radius

def color_correct(image, color):
    ''' Correct the image by setting the given color to black, and all other colors to white.'''
    pass # TODO
