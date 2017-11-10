"""Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
"""

from dronekit import connect, VehicleMode, LocationGlobal
from pymavlink import mavutil

import time
import logging


class VehicleController(object):
    """
    Navigation Controller interface base class.
    """

    def __init__(self, vehicle_resource='tcp:127.0.0.1:5760', logger=None):
        self._vehicle = connect(vehicle_resource, wait_ready=True)
        self._logger = logger
        self._location = self._vehicle.location.global_relative_frame
        self._vehicle.home_location = LocationGlobal(self._location.lat,
                                                     self._location.lon, self._location.alt)

        self._cmds = self._vehicle.commands
        self._cmds.clear()

        self.default_altitude = 3

    def initialize(self, vehicleConfig=None):
        """
        Initialize the vehicle.
        :param vehicleConfig:
        :return:
        """
        pass

    def takeoff(self):
        """
        Arms the copter object and flies to the default altitude. Follows
        recommended launch sequence detailed at this link:
        ---> http://python.dronekit.io/develop/best_practice.html
        """
        while not self._vehicle.is_armable:
            print 'Waiting for vehicle to initialize...'
            time.sleep(1)

        print 'Arming now'
        self._set_mode('GUIDED')
        self._vehicle.armed = True

        while not self._vehicle.armed:
            print 'Waiting for arming...'
            time.sleep(1)

        print 'Taking off!'
        self._vehicle.simple_takeoff(self.default_altitude)

        # Wait until the vehicle almost reaches target altitude
        while self._vehicle.location.global_relative_frame.alt < self.default_altitude*0.95:
            time.sleep(1)


    def takeoffTo(self, altitude):
        """
        Arms the copter object and flies to specified altitude.
        Follows recommended (safe) launch sequence detailed at this link:
        ---> http://python.dronekit.io/develop/best_practice.html

        :param altitude: Target height (m)
        """

        while not self._vehicle.is_armable:
            print 'Waiting for vehicle to initialize...'
            time.sleep(1)

        print 'Arming now'
        self._set_mode('GUIDED')
        self._vehicle.armed = True

        while not self._vehicle.armed:
            print 'Waiting for arming...'
            time.sleep(1)

        print 'Taking off!'
        self._vehicle.simple_takeoff(altitude)

        # Wait until the vehicle almost reaches target altitude
        while self._vehicle.location.global_relative_frame.alt < altitude*0.95:
            time.sleep(1)

    def land(self):
        """
        Land at current latitude/longitude by putting vehicle into LAND mode.
        """
        print 'Setting LAND mode...'
        self._set_mode('LAND')

    def moveTo(self, dx, dy, dz):
        pass # TODO: See issue #1 - implement using STABILIZE mode?

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

    def navigateTo(self, lat, lon, alt):
        ''' Navigate to the given GPS coordinate'''
        self._set_mode('GUIDED')
        gps_coord = LocationGlobal(lat, lon, alt)
        self._vehicle.simple_goto(gps_coord)

    def getLocation(self):
        ''' Report the vehicles current location'''
        print "Location:"
        print "Lat: %f" % self._location.lat
        print "Lon: %f" % self._location.lon
        print "Alt: %f" % self._location.alt

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
        :param mode: Integer designating the desired MAV mode
        """
        self._vehicle.mode = VehicleMode(mode)
