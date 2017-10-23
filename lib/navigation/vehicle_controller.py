'''Controller code for the FETCH navigation subsystem.

This file contains the interface definition for a high level
navigation controller.
'''

import abc
import logging

class VehicleController(object):
    ''' Navigation Controller interface base class.'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, vehicle_resource, logger=None):
        self._vehicle = vehicle_resource
        self._logger = logger

    @abc.abstractmethod
    def navigate_to(self, gps_coord):
        ''' Navigate to the given GPS coordinate'''
        pass

    @abc.abstractmethod
    def get_location(self):
        ''' Report the vehicles current location'''
        pass

    @abc.abstractmethod
    def _handle_command(self, command):
        ''' Handle a basic command'''
        pass

    def _log(self, message, level=logging.INFO):
        ''' Log to the navigation controllers specified logger'''
        if self._logger is not None:
            self._logger.log(level, message)

