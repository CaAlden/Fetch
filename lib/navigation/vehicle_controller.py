'''Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
'''

import logging

class VehicleController(object):
    ''' Navigation Controller interface base class.'''

    def __init__(self, vehicle_resource, logger=None):
        self._vehicle = vehicle_resource
        self._logger = logger

    def navigate_to(self, gps_coord):
        ''' Navigate to the given GPS coordinate'''
        pass

    def get_location(self):
        ''' Report the vehicles current location'''
        pass

    def _handle_command(self, command):
        ''' Handle a basic command'''
        pass

    def _log(self, message, level=logging.INFO):
        ''' Log to the navigation controllers specified logger'''
        if self._logger is not None:
            self._logger.log(level, message)

