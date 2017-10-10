import sys


try:
    import detection
except ImportError as e:
    print('Uh oh! {}'.format(e))
    if 'picamera' in str(e):
        print("\n\n=======\nDON'T run this test if you aren't on a Pi\n=======")
    sys.exit(1)

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
    'resolution': (640, 480)
}

instream = detection.PiStream(0, **cameraSettings)
outstream = detection.ImageViewer('Test')

procs = [detection.process_blur,
         detection.process_color,
         detection.process_circles]

def handle_circles(circles, img):
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        print("[DEBUG] -------- " + len(circles))
    return detection.draw_circles(img, circles)

print("Starting up!")
processor = detection.CircleProcessor(instream, outstream)

try:
    processor.start()
except KeyboardInterrupt as ke:
    s ys.exit(0)
