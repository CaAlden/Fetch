import yaml

ALTITUDE_MAX = 5     # in meters

def parseMissionConfig(missionPlanFilename):
    ''' Parse a mission configuration from the mission plan file'''
    with open(missionPlanFilename, 'r') as missionFile:
        rawConfig = yaml.load(missionFile)

    validateFormat(rawConfig)
    return rawConfig

def validateTitle(title):
    if title is None:
        return "\n Must specify a title"

def validateType(typeValue):
    typeValue = typeValue
    expectedTypes = ["deploy", "retrieve", "takeoff", "navigation", "mission"]
    if typeValue not in expectedTypes:
        return "\n- Type must be one of " + str(expectedTypes) + " got " + typeValue

def validateDescription(description):
    pass

def validateWaypoints(waypoints):
    if waypoints is None or len(waypoints) < 1:
        return "\n- Must specify at least 1 waypoint"
    else:
        completeReport = ''
        for latLon in waypoints:
            output = validateGPSCoord(latLon)
            if output is not None:
                completeReport += "\n" + output
        if len(completeReport) > 0:
            return completeReport

def validateGPSCoord(latLon):
    try:
        lat, lon, alt = tuple(map(lambda x: float(x.strip()), latLon.split(',')))
    except ValueError:
        return "- Malformed gps coordinate: " + latLon
    errStr = None
    if abs(lat) > 90:
        errStr = "- Latitude out of bounds: {}".format(lat)

    if abs(lon) > 180:
        if errStr is None:
            errStr = "- Longitude out of bounds: {}".format(lon)
        else:
            errStr += "\n- Longitude out of bounds: {}".format(lon)

    if abs(alt) > ALTITUDE_MAX:
        if errStr is None:
            errStr = "- Azimuth out of bounds: {}".format(az)
        else: 
            errStr += "\n- Azimuth out of bounds: {}".format(az)

    return errStr

def validateReturnHome(returnHome):
    if returnHome is None:
        return "\nMust specify Return Home"

VALIDATION_MAP  = {
    'title': validateTitle,
    'description': validateDescription,
    'waypoints': validateWaypoints,
    'type': validateType,
    'return home': validateReturnHome
}

def validateFormat(config, warnings=False):
    warnings = ''
    for key, value in config.items():
        if key.lower() in VALIDATION_MAP:
            out = VALIDATION_MAP[key.lower()](value)
            if out is not None:
                warnings += out

    if len(warnings) > 0:
        raise ValueError("Invalid Mission Config: {}".format(warnings))
