"""Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
"""

from dronekit import connect, VehicleMode, LocationGlobal

import time
import logging


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

    def initialize(self, vehicleConfig=None):
        """
        Initialize the vehicle.
        :param vehicleConfig:
        :return:
        """
        self._vehicle = connect(self._vehicle_resource, wait_ready=True)
        self._location = self._vehicle.location.global_relative_frame
        self._cmds = self._vehicle.commands
        self._cmds.clear()

    def takeoff(self):
        self.takeoffTo(self.default_altitude)

    def takeoffTo(self, altitude):
        """
        Arms the copter object and flies to specified altitude.
        Follows recommended (safe) launch sequence detailed at this link:
        ---> http://python.dronekit.io/develop/best_practice.html

        :param altitude: Target height (m)
        """
        self._set_mode('GUIDED')
        self._arm()
        self._vehicle.simple_takeoff(altitude)

        # Wait until the vehicle almost reaches target altitude
        while self._vehicle.location.global_relative_frame.alt < altitude*0.95:
            self._logger.debug("Taking off: Current Altitude %.3f", self._vehicle.location.global_relative_frame.alt)
            time.sleep(0.250)

    def land(self):
        """
        Land at current latitude/longitude by putting vehicle into LAND mode.
        """
        self._set_mode('LAND')

    def moveTo(self, dx, dy, dz):
        pass # TODO: See issue #1 - implement using STABILIZE mode?

    def returnHome(self):
        self._logger.warning("Returing home not yet supported!")

    def getVehicleStatus(self):
        """
        Display some basic vehicle attributes. Could be used to verify
        proper vehicle connection.
        """
        return {'type': self._vehicle._vehicle_type,
                'armed': self._vehicle.armed,
                'status': self._vehicle.system_status,
                'gps': self._vehicle.gps_0,
                'altitude': self._vehicle.location.global_relative_frame.alt}

    def navigateTo(self, lat, lon, alt):
        """
        Set GUIDED mode and navigate to the given GPS waypoint.
        """
        self._set_mode('GUIDED')
        gps_coord = LocationGlobal(lat, lon, alt)
        self._vehicle.simple_goto(gps_coord)

    def getLocation(self):
        """
        Report the vehicles current location.
        """
        return self._location.alt # TODO: shouldn't this give back more than just alt?

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
        self._vehicle.mode = VehicleMode(mode)

    def _arm(self):
        """
        Safely arms the drone.
        """
        while not self._vehicle.is_armable:
            time.sleep(1)

        self._vehicle.armed = True

        while not self._vehicle.armed:
            time.sleep(1)

    def _disarm(self):
        """
        Safely disarms the drone.
        """
        self._vehicle.armed = False
        while self._vehicle.armed:
            time.sleep(1)
