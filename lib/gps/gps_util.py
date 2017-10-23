import re

GPGLL_RE = r'\$GPGLL,(\d\d)(\d\d\.\d\d\d\d\d),([NS]),(\d\d\d)(\d\d\.\d\d\d\d\d),([WE]),(\d\d)(\d\d)(\d\d\.\d\d),([AV]),A\*(..)'
LATITUDE_DEGREES = 1
LATITUDE_MINUTES = 2
LATITUDE_HEADING = 3
LONGITUDE_DEGREES = 4
LONGITUDE_MINUTES = 5
LONGITUDE_HEADING = 6
TIME_HOURS = 7
TIME_MINUTES = 8
TIME_SECONDS = 9
VALIDITY = 10
CHECKSUM = 11

class GPSCoord():

    @staticmethod
    def from_GPGLL_string(in_string):
        match = re.search(GPGLL_RE, in_string)

        if match is None or match.group(VALIDITY) != 'A':
            raise RuntimeError('Could not parse input string "{}"'.format(repr(in_string)))

        lat = float(match.group(LATITUDE_DEGREES)) + (float(match.group(LATITUDE_MINUTES)) / 60.0)

        if match.group(LATITUDE_HEADING) == 'S':
            lat = -lat
        elif match.group(LATITUDE_HEADING) != 'N':
            raise RuntimeError('Could not parse input string "{}"'.format(repr(in_string)))

        lon = float(match.group(LONGITUDE_DEGREES)) + (float(match.group(LONGITUDE_MINUTES)) / 60.0)
        if match.group(LONGITUDE_HEADING) == 'W':
            lon = -lon
        elif match.group(LONGITUDE_HEADING) != 'E':
            raise RuntimeError('Could not parse input string "{}"'.format(repr(in_string)))

        time = (int(match.group(TIME_HOURS)), int(match.group(TIME_MINUTES)), float(match.group(TIME_SECONDS)))


        return GPSCoord(lat, lon, time)

    def __init__(self, latitude, longitude, time):
        self.latitude = latitude
        self.longitude = longitude
        self.time = time

    def lat_long(self):
        return (self.latitude, self.longitude)
