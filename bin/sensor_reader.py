#!/usr/bin/python3

import yaml
import serial
import lib.sensor
import lib.config

# fetch data from serial line
def readSerial():

    """
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
    except:
        ser = serial.Serial('/dev/ttyUSB1', baudrate=9600)
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

            #res[sensor_id] = getCalibVal(sensor_id, value)

            print("%d %d" %(sensor_id, value))


        line = ser.readline().decode("ascii")

    return res



#def calibrate(values):
#    global config
    
config = lib.config.read()
print(config)

print(readSerial())
