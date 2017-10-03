#!/usr/bin/env python

"""
-- test_mission.py --

Basic script to generate a series of waypoints and create a basic mission plan.

********* CONFIGURATION USED *********

  SOFTWARE     |     DESCRIPTION
---------------------------------------
QGroundControl |  Ground Station GUI
---------------------------------------
JMAVSim        | Drone Simulator (SITL)


* NOTE: Used a different JMAVSim home position configuration for this script.
    1. To change home position, navigate to:
        PX4 firmware -> jMAVSim -> src -> me -> drton -> jmavsim -> Simulator.java

    2. Within Simulator.java, change LatLonAlt variable to the Seattle ref point:
        public static LatLonAlt DEFAULT_ORIGIN_POS = new LatLonAlt(47.592182, -122.316031, 86);


********* BEFORE RUNNING THIS SCRIPT *********

Start the simulator using the following command:
    --->  make posix_sitl_default jmavsim
            ** (Must be in cloned PX4 firmware directory)

If configuring QGroundControl for the first time:
    - Go to Q --> Comm Links --> Add
    - Add a UDP connection on port 14550, then connect.


********* USEFUL LINKS *********

Command Structure
    ---> http://python.dronekit.io/automodule.html#dronekit.Command

"""

from dronekit import connect, LocationGlobalRelative, LocationGlobal, Command
from pymavlink import mavutil

import time
import math

MAV_MODE_AUTO = 4


def px4_set_mode(mav_mode):
    """
    Set vehicle mode.
    Vehicle mode switching is not yet supported for PX4 using Dronekit, so no list of valid
    mav modes exists...
    :param mav_mode:
    """

    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
                                               mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                               mav_mode, 0, 0, 0, 0, 0, 0)


def init_test_mission(location):
    """
    Initial testing of mission planning/waypoint setting using Dronekit.
    Clears any existing missions first.

    :param location: LocationGlobal object containing GPS coordinates
    """

    cmds = vehicle.commands
    cmds.clear()

    # Add takeoff command in case copter is not yet airborne
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, 47.59218, -122.316031, location.lat+20))

    # Spawn waypoint object
    waypoint = LocationGlobal(47.5910820, -122.3159810, 40)

    # Add command to navigate to waypoint objects
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, waypoint.lat, waypoint.lon,
                      waypoint.alt))

    # Land
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND,
                  0, 1, 0, 0, 0, 0, 47.5911820, -122.314, location.alt))

    cmds.upload()
    print 'Mission initialized; commands uploaded'


def display_vehicle_stats():
    """
    Temp function to display some basic vehicle attributes. Could be used to verify
    proper vehicle connection.
    """
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt


def dist_to_current_waypoint():
    """
    Gets distance in meters to the current waypoint. Returns None for home location.
    :return: distance_to_point
    """
    next_waypoint = vehicle.commands.next
    if next_waypoint == 0:
        return None
    mission_item = vehicle.commands[next_waypoint-1]
    latitude = mission_item.x
    longitude = mission_item.y
    altitude = mission_item.z
    target_location = LocationGlobalRelative(latitude, longitude, altitude)
    distance_to_point = get_distance_meters(vehicle.location.global_frame, target_location)

    return distance_to_point


def get_distance_meters(location1, location2):
    """
    Returns the ground distance in meters between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
            ---> https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def takeoff(target_altitude):
    #TODO: adapt for PX4, this seems to only be supported by Ardupilot
    """
    Arms the copter object and flies to specified altitude.
    Follows recommended (safe) launch sequence detailed at this link:
        ---> http://python.dronekit.io/develop/best_practice.html

    :param target_altitude: Target height (m)
    """

    while not vehicle.is_armable:
        print 'Waiting for vehicle to initialize...'
        time.sleep(1)

    print 'Arming now'
    # vehicle.mode = VehicleMode('GUIDED')
    vehicle.armed = True

    while not vehicle.armed:
        print 'Waiting for arming...'
        time.sleep(1)

    print 'Taking off!'
    vehicle.simple_takeoff(target_altitude)

    # Wait until the vehicle almost reaches target altitude
    while vehicle.location.global_relative_frame.alt < target_altitude*0.95:
        time.sleep(1)


if __name__ == '__main__':

    vehicle = connect('127.0.0.1:14540', wait_ready=True)

    home_position_set = False

    # Create a message listener for home position fix
    @vehicle.on_message('HOME_POSITION')
    def listener(self, name, home_position):
        global home_position_set
        home_position_set = True

    # Wait for JMAVSim to finish initializing
    while not home_position_set:
        print "Waiting for home position..."
        time.sleep(1)

    display_vehicle_stats()

    # Change to auto mode to prepare for mission upload
    px4_set_mode(MAV_MODE_AUTO)
    print 'Vehicle mode set to AUTO'
    time.sleep(5)

    # Upload test commands
    init_test_mission(vehicle.location.global_relative_frame)

    # Start mission
    vehicle.armed = True

    # Monitor mission execution
    next_waypoint = vehicle.commands.next
    while next_waypoint < len(vehicle.commands):
        if vehicle.commands.next > next_waypoint:
            display_seq = vehicle.commands.next+1
            print "Moving to waypoint %s" % display_seq
            next_waypoint = vehicle.commands.next
        time.sleep(1)

    # Wait for the vehicle to land
    while vehicle.commands.next > 0:
        time.sleep(1)

    # Disarm vehicle
    vehicle.armed = False
    time.sleep(1)

    # Close vehicle object before exiting script
    vehicle.close()

