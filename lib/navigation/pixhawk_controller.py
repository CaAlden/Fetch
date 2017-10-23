from vehicle_controller import VehicleController

class PixhawkController(VehicleController):

    def __init__(self):
        vehicle = None # TODO: Create mavlink connection to pixhawk
        super().__init__(vehicle, logger=None)

    def _handle_command(self, command):
        ''' Send commands into the pixhawk.'''
        pass # TODO: Send commands into pixhawk.

    def get_location(self):
        ''' Get the location of the vehicle in the sim.'''
        return None # TODO: get location

    def navigate_to(self, gps_coord):
        ''' Navigate the simulator to a given coord'''
        pass # TODO. Figure out the command to send.
