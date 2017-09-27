import sys


try:
    import detection
except ImportError as e:
    print('Uh oh! {}'.format(e))
    if 'picamera' in str(e):
        print("\n\n=======\nDON'T run this test if you aren't on a Pi\n=======")
    sys.exit(1)

imgfile = sys.argv[1:]

instream = detection.PiCameraStream(imgfile)
outstream = detection.ImageViewer('Test')

procs = [lambda x: x]

processor = detection.ProcessAccumulator(instream, outstream, procs)

processor.start()
