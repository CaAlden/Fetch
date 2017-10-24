'''Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
'''

import logging

class VehicleController(object):
    ''' Navigation Controller interface base class.'''

    def __init__(self, vehicleResource, logger=None):
        self._vehicle = vehicleResource
        self._logger = logger

    def initialize(self, vehicleConfig=None):
        '''Initialize the vehcile.'''
        pass

    def takeoff(self):
        pass

    def takeoffTo(self, altitude):
        pass

    def land(self):
        pass

    def moveTo(self, dx, dy, dz):
        pass # TODO: See issue #1

    def getVehicleStatus(self):
        pass

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

