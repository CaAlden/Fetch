#!/usr/bin/python3
# add the library directory to the path for this script.
import sys
import os
import time
from collections import namedtuple

lib_path = os.path.dirname(os.path.realpath(__file__)) + "/lib"
sys.path.insert(0, lib_path)


## Beginning of actual script
from signal import SIGKILL

from functools import partial
import argparse
import logging
import socket

import yaml

from navigation import VehicleController, form_waypoint
from mission_config import parseMissionConfig
import watchdog

LatLon = namedtuple('LatLon', ['lat', 'lon'])

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="The config file for the mission controller.")
    parser.add_argument('mission', help="The mission configuration to run.")
    parser.add_argument('--heartbeat_srv', help="Address and port of the heartbeat sender.")

    return parser.parse_args()

def loadConfiguration(configFilename):
    """ Load the configuration file.
        Args:
            configFilename - The name of the yaml file containing the mission run configurations."""
    with open(configFilename, 'r') as configFile:
        return yaml.load(configFile)

def doReturnHome(drone, missionConf, waypoint):
    if missionConf['Return Home']:
        print(waypoint)
        genericGoToLandMission(drone, waypoint)
        drone.startMission()

def genericMission(drone, missionConf, missionStrategy):
    drone.takeoff()
    missionStrategy(drone, missionConf)
    doReturnHome(drone, missionConf)
    drone.land()
    drone.startMission()

def genericGoToLandMission(drone, waypoint):
    drone.clearMission()
    drone.takeoff()
    drone.navigateTo(waypoint)
    drone.land(waypoint.lat, waypoint.lon)
    drone.startMission()

def handleNavigationMission(drone, missionConf, wayPointTask=None):
    def navStrat(drone, missionConf):
        for waypoint in missionConf['Waypoints']:
            waypoint = form_waypoint(waypoint)
            drone.navigateTo(waypoint)
            if wayPointTask is not None:
                wayPointTask(drone, missionConf)

    genericMission(drone, missionConf, navStrat)

def handleDeployRetrieveMission(drone, missionConf, waypointTask=None):
    for waypoint in missionConf['Waypoints']:
        waypoint = form_waypoint(waypoint)
        genericGoToLandMission(drone, waypoint)
        if waypointTask is not None:
            waypointTask(drone, missionConf)

    # doReturnHome(drone, missionConf, home_waypoint)

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
        # TODO: deploy node here
        # while(!nodeDeployed):
        time.sleep(25)  # placeholder to delay mission

    handleDeployRetrieveMission(drone, missionConf, deployWaypointHandler)

def handleRetrieveMission(drone, missionConf):
    def retrieveWaypointHandler(drone, missionConf):
        # TODO: pickup node here
        # while (!nodeRetrieved):
        time.sleep(25) # placeholder to delay mission

    handleDeployRetrieveMission(drone, missionConf, retrieveWaypointHandler)

def handleMission(drone, missionConf):
    MISSIONS = {
        'navigation': handleNavigationMission,
        'takeoff': handleTakeoffMission,
        'mission': handleDefaultMission,
        'deploy': handleDeployMission,
        'retrieve': handleRetrieveMission
    }
    MISSIONS[missionConf['Type']](drone, missionConf)

def parseSockInfo(socketStr):
    s = socketStr.split(':')
    return s[0], int(s[1])

def getHeartbeatSocket(addrInfo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addrInfo)
    sock.settimeout(1)
    return sock

def on_success(hb):
    ''' What to do when we receive a hb'''
    logging.info("Got hb: %s", str(hb))

def on_err(e):
    ''' handle an error on the drone.'''
    logging.error('Got %s', e)

def on_timeout(process, drone=None):
    ''' Handle a heartbeat timeout'''
    os.kill(process.pid, SIGKILL)
    drone.clearMission()
    drone.land(drone.current_lat, drone.current_lon)
    drone.update()

def main():

    args = getArgs()
    config = loadConfiguration(args.config)

    drone = VehicleController(vehicle_resource=config['vehicle'])
    missionConf = parseMissionConfig(args.mission)

    logging.basicConfig(filename=missionConf['Name'] + '.log',
                        filemode='w',
                        level=logging.DEBUG)

    logging.info("[Name]: %s", missionConf['Name'])
    logging.info("[Description]: %s", missionConf['Description'])
    logging.info("[Type]: %s", missionConf['Type'])

    #drone.initialize()
    if args.heartbeat_srv is None:
        handleMission(drone, missionConf)
    else:
        sockInfo = parseSockInfo(args.heartbeat_srv)
        sock = getHeartbeatSocket(sockInfo)
        mission = partial(handleMission, drone, missionConf)
        timeout_handler = partial(on_timeout, drone=drone)
        watchdog.heartbeat_watchdog(mission, sock, 1, on_success, on_err, on_timeout=timeout_handler)

if __name__ == '__main__':
    main()
