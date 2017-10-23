from vehicle_controller import VehicleController

class SimulatorController(VehicleController):

    def __init__(self):
        vehicle = None # TODO: Create simulator connection.
        super().__init__(vehicle, logger=None)

    def _handle_command(self, command):
        ''' Send commands into the simulator.'''
        pass # TODO: Send commands into sim.

    def get_location(self):
        ''' Get the location of the vehicle in the sim.'''
        return None # TODO: get location

    def navigate_to(self, gps_coord):
        ''' Navigate the simulator to a given coord'''
        pass # TODO. Figure out the command to send.
