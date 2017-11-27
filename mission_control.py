#!/usr/bin/python3
# add the library directory to the path for this script.
import sys
import os
lib_path = os.path.dirname(os.path.realpath(__file__)) + "/lib"
sys.path.insert(0, lib_path)


## Beginning of actual script
import argparse
import logging
import yaml

from navigation import VehicleController
from mission_config import parseMissionConfig

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="The config file for the mission controller.")
    parser.add_argument('mission', help="The mission configuration to run.")

    return parser.parse_args()

def loadConfiguration(configFilename):
    """ Load the configuration file.
        Args:
            configFilename - The name of the yaml file containing the mission run configurations."""
    with open(configFilename, 'r') as configFile:
        return yaml.load(configFile)

def doReturnHome(drone, missionConf):
    if missionConf['Return Home']:
        drone.returnHome()

def genericMission(drone, missionConf, missionStrategy):
    drone.takeoff()
    missionStrategy(drone, missionConf)
    doReturnHome(drone, missionConf)
    drone.land()

def handleNavigationMission(drone, missionConf, wayPointTask=None):
    def navStrat(drone, missionConf):
        for lat, lon, alt in missionConf['Waypoints']:
            drone.navigateTo(lat, lon, alt)
            if wayPointTask is not None:
                wayPointTask(drone, missionConf)

    genericMission(drone, missionConf, navStrat)

def handleTakeoffMission(drone, missionConf):
    def doNothing(drone, missionConf):
        pass

    genericMission(drone, missionConf, doNothing)

def handleDefaultMission(drone, missionConf):
    def missionWaypointHandler(drone, missionConf):
        pass # TODO: Actually do something at each waypoint

    handleNavigationMission(drone, missionConf, wayPointTask=missionWaypointHandler)

def handleDeployMission(drone, missionConf):
    def deployWaypointHandler(drone, missionConf):
        pass # TODO: Actually do something at each waypoint

    handleNavigationMission(drone, missionConf, wayPointTask=deployWaypointHandler)

def handleRetrieveMission(drone, missionConf):
    def retrieveWaypointHandler(drone, missionConf):
        pass # TODO: Actually do something at each waypoint

    handleNavigationMission(drone, missionConf, wayPointTask=retrieveWaypointHandler)

def handleMission(drone, missionConf):
    MISSIONS = {
        'navigation': handleNavigationMission,
        'takeoff': handleTakeoffMission,
        'mission': handleDefaultMission,
        'deploy': handleDeployMission,
        'retrieve': handleRetrieveMission
    }
    MISSIONS[missionConf['Type']](drone, missionConf)

def main():

    args = getArgs()
    config = loadConfiguration(args.config)

    drone = VehicleController(vehicle_resource=config['vehicle'])
    missionConf = parseMissionConfig(args.mission)

    logging.info("[Name]: %s", missionConf['Name'])
    logging.info("[Description]: %s", missionConf['Description'])
    logging.info("[Type]: %s", missionConf['Type'])

    # TODO: Establish heartbeat if that option is given.
    drone.initialize()
    handleMission(drone, missionConf)

if __name__ == '__main__':
    main()
