import sys
import math
import numpy as np


try:
    import detection
except ImportError as e:
    print('Uh oh! {}'.format(e))
    if 'picamera' in str(e):
        print("\n\n=======\nDON'T run this test if you aren't on a Pi\n=======")
    sys.exit(1)

img_height = 640
img_width = 480

cameraSettings = {
    'hflip': True,
    'vflip': True,
    'sharpness': 0,
    'contrast': 0,
    'saturation': 0,
    'ISO': 0,
    'video_stabilization': False,
    'exposure_compensation': 0,
    'exposure_mode': 'auto',
    'meter_mode': 'average',
    'awb_mode': 'auto',
    'image_effect': 'none',
    'color_effects': None,
    'rotation': 0,
    'crop': (0.0, 0.0, 1.0, 1.0),
    'resolution': (img_height, img_width)
}

instream = detection.PiStream(0, **cameraSettings)
outstream = detection.ObjectStream(None)

procs = [detection.process_blur,
         detection.process_color,
         detection.process_circles]

known_radius = .112 # meters
focal_length = 3.6e-3 # meters

def handle_circles(circles, img):
    if circles is not None:
        usable = np.round(circles[0, :]).astype("int")
        for x, y, r in usable:
            distance = (known_radius) / (r * focal_length)
            angle = (180 / math.pi) * math.atan((y - (img_height / 2)) / (x - (img_width / 2)))
            print(x, y, r)
            print('circle found at {} m angle {} degrees'.format(distance, angle))

print("Starting up!")
processor = detection.CircleProcessor(instream, outstream,circle_handler=handle_circles)

try:
    processor.start()
except KeyboardInterrupt as ke:
    sys.exit(0)
