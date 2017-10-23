import sys

import detection

imgfile = sys.argv[1]

instream = detection.ImageStream(imgfile)
outstream = detection.ImageViewer('Test')

procs = [detection.process_blur,
         detection.process_color,
         detection.process_circles]

processor = detection.ProcessAccumulator(instream, outstream, procs)
processor.start()

