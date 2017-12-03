"""Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
"""

from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil
from .nav_util import form_waypoint, get_location_bounds

import time
import logging

AUTO = 4

class VehicleController(object):
    """
    Navigation Controller interface base class.
    """

    def __init__(self, vehicle_resource='tcp:127.0.0.1:5760', logger=None):
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self._vehicle_resource = vehicle_resource
        self.default_altitude = 3
        self._initialized = False

    def initialize(self, vehicleConfig=None):
        """
        Initialize the vehicle.
        :param vehicleConfig:
        :return:
        """
        self._vehicle = connect(self._vehicle_resource, wait_ready=True)
        self._cmds = self._vehicle.commands
        self.clearMission()
        self._initialized = True

    def _assertInitialized(self):
        if not self._initialized:
            raise RuntimeError("{} not initialized!".format(self._vehicle_resource))

    @property
    def current_lat(self):
        self._assertInitialized()
        return self._vehicle.location._lat

    @property
    def current_lon(self):
        self._assertInitialized()
        return self._vehicle.location._lon

    @property
    def current_alt(self):
        self._assertInitialized()
        return self._vehicle.location._alt

    @property
    def home_position(self):
        self._assertInitialized()
        return self._vehicle.home_location

    def takeoff(self):
        self._assertInitialized()
        self.takeoffTo(self.default_altitude)

    def takeoffTo(self, altitude):
        self._assertInitialized()
        self._cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, self.current_lat,
                        self.current_lon, float(altitude)))

    def land(self, lat, lon):
        """
        Land at specified latitude/longitude by putting vehicle into LAND mode.
        """
        self._assertInitialized()
        self._cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, float(lat),
                      float(lon), 0.0))

    def moveTo(self, dx, dy, dz):
        self._assertInitialized()
        # TODO: See issue #1 - implement using STABILIZE mode?

    def returnHome(self):
        """
        Return to the home position (where vehicle was armed).
        NOTE: The value parameter RTL_MIN from within GCS configuration will determine what altitude the drone
        will take off to when returning home. The default is 15 m.
        """

        self._assertInitialized()
        self._cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 1, 0, 0, 0, 0, 0, 0, 0))

    def getVehicleStatus(self):
        """
        Display some basic vehicle attributes. Could be used to verify
        proper vehicle connection.
        """
        self._assertInitialized()
        return {'type': self._vehicle._vehicle_type,
                'armed': self._vehicle.armed,
                'status': self._vehicle.system_status,
                'gps': self._vehicle.gps_0,
                'altitude': self.current_alt}

    def navigateTo(self, waypoint):
        """
        Navigate to the given GPS waypoint.
        """
        self._assertInitialized()
        self._cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                               mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                               float(waypoint.lat), float(waypoint.lon), float(waypoint.alt)))

    def startMission(self):
        self.update()
        self._arm()
        self._set_mode(AUTO)
        self._cmds.next = 1

    def clearMission(self):
        self._cmds.clear()
        self.update()

    def update(self):
        self._cmds.upload()

    def getLocation(self):
        """
        Report the vehicles current location.
        """
        self._assertInitialized()
        return {'lat': self.current_lat,
                'lon': self.current_lon,
                'alt': self.current_alt}

    def reachedLocation(self, location):
        """
        Determines if the vehicle has reached the given location coordinates.
        :param location: LocationGlobal object specifying the location that the drone should reach.
        :return: Bool indicating whether the location has been reached (within error bounds).
        """
        self._assertInitialized()
        bounds = get_location_bounds(location)
        if (self.current_lat > bounds.lat.max or self.current_lat < bounds.lat.min) and \
            (self.current_lon > bounds.lon.max or self.current_lon < bounds.lon.min):
            return False
        else:
            return True

    def _log(self, message, level=logging.INFO):
        """
        Log in to the navigation controller's specified logger.
        """
        if self._logger is not None:
            self._logger.log(level, message)

    def _set_mode(self, mode):
        """
        Set vehicle mode.
        :param mode: Integer designating the desired MAV mode
        """
        self._assertInitialized()
        self._vehicle.mode = VehicleMode(mode)

    def _arm(self):
        """
        Safely arms the drone.
        """
        self._assertInitialized()
        self._vehicle.armed = True

        while not self._vehicle.armed:
            time.sleep(1)

    def _disarm(self):
        """
        Safely disarms the drone.
        """
        self._assertInitialized()
        self._vehicle.armed = False

        while self._vehicle.armed:
            time.sleep(1)
