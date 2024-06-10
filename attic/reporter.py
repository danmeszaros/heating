#!/usr/bin/python3
#
# this program reads both serial usb data, then converts raw values using calibrations
# to celsius and sends data over http to grafana
#

import sys
import serial
import http.client
import datetime

calibref = [-20, -1, 26, 50, 82, 112]

calibval = [
            [434, 858, 1441, 1992, 2634, 3128],
            [434, 864, 1452, 2003, 2656, 3224],
            [460, 886, 1478, 2014, 2661, 3259],
            [477, 901, 1492, 2029, 2675, 3270],
            [466, 889, 1480, 2013, 2659, 3253],
            [460, 885, 1475, 2006, 2655, 3250],
            [464, 885, 1476, 2010, 2659, 3247],
            [453, 880, 1470, 2002, 2649, 3240]
        ]

def getCalibVal(sensor_id, val):
    res = -100
    row = calibval[sensor_id]

    i = 0
    while val > row[i]:
        i = i + 1
        if i == 4:
            break

    # print("%d %d %d" %(sensor_id, val, i))

    c_low = calibref[i]
    c_high = calibref[i+1]

    low = float(row[i])
    high = float(row[i+1])
    val = float(val)

    ratio = (val - low) / (high - low)
    res = c_low + ratio * (c_high - c_low)

    return round(res, 1)

def getTemps():

    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
    except:
        ser = serial.Serial('/dev/ttyUSB1', baudrate=9600)


    line = ser.readline().decode("ascii")

    res = {}

    while line:
        line = line[0:-1]
        if len(line) > 5 and line[0:5] == "VALUE":
            l = line[5:]
            arr = l.split('=')
            sensor_id = int(arr[0])
            value = int(arr[1])

            res[sensor_id] = getCalibVal(sensor_id, value)

            # print("%d %d" %(sensor_id, getCalibVal(sensor_id, value)))

            if len(res) == 8:
                return res


        line = ser.readline().decode("ascii")

def sendValue(sensor_id, value):
    path = "/report.py?id=%d&temp=%.1f" %(sensor_id + 1000, value)
    try:
        connection = http.client.HTTPConnection("www.dna1.cz")
        connection.request("GET", path)
        response = connection.getresponse()
        connection.close()
        print(path)

    except:
        pass

while 1 ==1:
    res = getTemps()

    outf = open("log.txt", "a")
    outf.write(str(datetime.datetime.now()) + " ")
    outf.write(str(res) + "\n")
    outf.close()

    for k in res.keys():
        sendValue(k, res[k])
    break

