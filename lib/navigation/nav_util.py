"""
Library to store helper functions for navigation
"""

import math
from collections import namedtuple
from dronekit import LocationGlobal

LOCATION_ERROR = .0000001


def form_waypoint(waypoint_str):
    """
    Forms the LocationGlobal waypoint object from an inputted waypoint string.
    :return: LocationGlobal object containing lat, lon and alt.
    """
    lat,lon,alt = waypoint_str.split(',')
    return LocationGlobal(float(lat), float(lon), float(alt))


def get_location_bounds(location):
    """
    Determines the min/max coordinate bounds for latitude/longitude of a given location. This will be
    used to determine if the vehicle is close enough to the coordinate it is trying to reach.
    :param location: LocationGlobal object that represents the target location of the drone.
    :return: NamedTuple object that contains lat/lon and their respective min/max values.
    """
    CoordinateBound = namedtuple('CoordinateBound', ['min', 'max'])
    lat_error = location.lat * LOCATION_ERROR
    lon_error = location.lon * LOCATION_ERROR
    lat_bound = CoordinateBound(location.lat-lat_error, location.lat+lat_error)
    lon_bound = CoordinateBound(location.lon-lon_error, location.lon+lon_error)

    Bounds = namedtuple('Bounds', ['lat', 'lon'])
    return Bounds(lat_bound, lon_bound)


def get_distance_meters(location1, location2):
    """
    Returns the ground distance in meters between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles.
    :param location1: LocationGlobal object.
    :param location2: LocationGlobal object.
    :return: Distance between location1 and location2 (m).
    """
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def dist_to_waypoint(vehicle, waypoint):
    """
    Gets distance in meters to the current waypoint. Returns None for home location.
    :param: vehicle: Vehicle object.
    :param: waypoint: String containing comma-separated latitude, longitude and altitude.
    :return: distance_to_point: Distance to waypoint from current location (m).
    """
    current_location = LocationGlobal(vehicle.current_lat, vehicle.current_lon, vehicle.current_alt)
    target_location = form_waypoint(waypoint)
    distance_to_point = get_distance_meters(current_location, target_location)

    return distance_to_point

