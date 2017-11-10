"""Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
"""

from dronekit import connect, Command
from pymavlink import mavutil

import time
import logging

MAV_MODE_AUTO = 4  # temp


class VehicleController(object):
    """
    Navigation Controller interface base class.
    """

    def __init__(self, vehicle_resource='127.0.0.1:14540', logger=None):
        self._vehicle = connect(vehicle_resource, wait_ready=True)
        self._logger = logger
        self._location = self._vehicle.location.global_relative_frame

        self._cmds = self._vehicle.commands
        self._cmds.clear()

    def initialize(self, vehicleConfig=None):
        """
        Initialize the vehicle.
        :param vehicleConfig:
        :return:
        """
        pass

    def takeoff(self):
        pass

    def takeoffTo(self, altitude):
        """
        Take off to specified altitude in meters. Assumes takeoff from current
        latitude/longitude.
        :param altitude: (m).
        """
        # TODO; implement this later for safe takeoff
        # while not self._vehicle.is_armable:
        #     print 'Waiting for vehicle to initialize...'
        #     time.sleep(1)

        print 'Arming now'
        # self._set_mode(MAV_MODE_AUTO)
        self._vehicle.armed = True
        while not self._vehicle.armed:
            print 'Waiting for arming...'
            time.sleep(1)

        print 'Taking off!'
        self._vehicle._master.mav.command_long_send(self._vehicle._master.target_system,
                                                    self._vehicle._master.target_component,
                                                    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                                    0, 0, 0, 0, 0, float(self._location.lat),
                                                    float(self._location.lon),
                                                    float(altitude))

        # Wait until vehicle approximately reaches target altitude
        # while self._location.alt < altitude*0.95:
        #     time.sleep(1)

    def land(self):
        """
        Land at current latitude/longitude.
        """
        self._vehicle._master.mav.command_long_send(self._vehicle._master.target_system,
                                                    self._vehicle._master.target_component,
                                                    mavutil.mavlink.MAV_CMD_NAV_LAND,
                                                    0, 0, 0, 0, 0, float(self._location.lat),
                                                    float(self._location.lon),
                                                    self._vehicle.home_location.alt)

        while self._location.alt > self._vehicle.home_location.alt:
            time.sleep(1)

    def moveTo(self, dx, dy, dz):
        pass # TODO: See issue #1

    def getVehicleStatus(self):
        """
        Display some basic vehicle attributes. Could be used to verify
        proper vehicle connection.
        """
        print " Type: %s" % self._vehicle._vehicle_type
        print " Armed: %s" % self._vehicle.armed
        print " System status: %s" % self._vehicle.system_status.state
        print " GPS: %s" % self._vehicle.gps_0
        print " Alt: %s" % self._vehicle.location.global_relative_frame.alt

    def navigateTo(self, gpsCoord):
        ''' Navigate to the given GPS coordinate'''
        pass

    def getLocation(self):
        ''' Report the vehicles current location'''
        pass

    def _handleCommand(self, command):
        ''' Handle a basic command'''
        pass

    def _log(self, message, level=logging.INFO):
        ''' Log to the navigation controllers specified logger'''
        if self._logger is not None:
            self._logger.log(level, message)

    def _set_mode(self, mode):
        """
        Set vehicle mode.
        Vehicle mode switching is not yet supported for PX4 using Dronekit, so no list of valid
        mav modes exists...
        :param mode: Integer designating the desired MAV mode
        """
        self._vehicle._master.mav.command_long_send(self._vehicle._master.target_system,
                                                    self._vehicle._master.target_component,
                                                    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
                                                    0, mode, 0, 0, 0, 0, 0, 0)

