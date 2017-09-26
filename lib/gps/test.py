import gps_util
import gmplot
import serial
import sys

DEV = '/dev/ttyUSB0'

if len(sys.argv) == 2:
    DEV = sys.argv[1]

print('Trying to plot GPS coords from ' + DEV)

try:
    port = serial.Serial(DEV, 9600, timeout=10)
except:
    print('Could not open serial port "{}"'.format(DEV))
    sys.exit(1)

plotter = gmplot.GoogleMapPlotter(42.3398, -71.0892, 16)

i = 0
latitudes = []
longitudes = []
while i < 10:
    try:
        coord = gps_util.GPSCoord.from_GPGLL_string(port.readline().decode())
        latitudes.append(coord.latitude)
        longitudes.append(coord.longitude)
        i += 1
        print('\nGot data point ' + str(i))
    except RuntimeError as e:
        print(".", end='')

port.close()


plotter.scatter(latitudes, longitudes , 'r', marker=True)
plotter.draw('example.html')

