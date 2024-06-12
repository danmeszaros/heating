#!/usr/bin/python3

import serial
import lib.sensor
import lib.config
import pprint
import logging as log

# fetch data from serial line
def readSerial():

    """
    baudrate = config['serial']['baudrate']
    ser = None

    for dev in config['serial']['device']:
        try:
            ser = serial.Serial(dev, baudrate = baudrate)
            break
        except:
            pass

    if ser == None:
        log.error("no serial device found")
        return {}

    """

    #"""
    # for testing:
    ser = open("/dev/stdin", "rb")
    #"""

    line = ser.readline().decode("ascii")

    res = {}

    # wait for BEGIN
    while line:
        if line == "BEGIN\n":
            break

        line = ser.readline().decode("ascii")

    line = ser.readline().decode("ascii")

    while line:
        line = line[0:-1]

        if line == "END":
            break

        if len(line) > 5 and line[0:5] == "VALUE":
            l = line[5:]
            arr = l.split('=')
            sensor_id = int(arr[0])
            value = int(arr[1])

            res[sensor_id] = value

        line = ser.readline().decode("ascii")

    return res

def getSensorDetails(sid):
    for sensor in config["sensors"]:
        if sensor['sourceId'] == sid:
            return sensor
    return None

def getCalibVal(val, calibref, calibrations):
    res = -100

    i = 0
    while val > calibrations[i]:
        i = i + 1
        if i == 4:
            break

    # print("%d %d %d" %(sensor_id, val, i))

    c_low = calibref[i]
    c_high = calibref[i+1]

    low = float(calibrations[i])
    high = float(calibrations[i+1])
    val = float(val)

    ratio = (val - low) / (high - low)
    res = c_low + ratio * (c_high - c_low)

    return round(res, 1)


def recalcVals(vals):
    calibref = [int(x) for x in config['calibrationPoints'].split(',')]

    res={}

    for (sid, rawVal) in vals.items():

        # print("%d %d" %(sid, rawVal))

        sdetails = getSensorDetails(sid)

        if sdetails:
            if sdetails['type'] == 'analog':
                calibrations = [int(x) for x in sdetails['calibrations'].split(',')]
                val = getCalibVal(rawVal, calibref, calibrations)

                res[sdetails['name']] = val

            elif sdetails['type'] == 'digital':
                # keep original value
                res[sdetails['name']] = rawVal

        else:
            log.warning("unknown sensor '%d'", sid)

    return res


if __name__ == "__main__":

    config = lib.config.read()
    # pprint.pprint(config)

    readings = readSerial()

    calibratedVals = recalcVals(readings)

    for (dev, val) in calibratedVals.items():
        lib.sensor.setValue(config, dev, val)

