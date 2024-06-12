#!/usr/bin/python3

import logging as log
import http.client
import datetime
import lib.sensor
import lib.config

def logValue(sensorId, value):
    fname = config['appRoot'] + config['reporter']['valueLog']

    try:
        outf = open(fname, "a")
        outf.write(str(datetime.datetime.now()) + " ")
        outf.write("%s %.1f" %(sensorId, value) + "\n")
        outf.close()
    except Exception as e:
        log.error("failed to write to log '%s': %s", fname, repr(e))

def sendValue(sensor_id, value):
    path = "/report.py?id=%d&temp=%.1f" %(sensor_id, value)
    try:
        connection = http.client.HTTPConnection(config['reporter']['url'])
        connection.request("GET", path)
        response = connection.getresponse()
        connection.close()

    except:
        pass



if __name__ == "__main__":
    config = lib.config.read()

    for item in config['reporter']['mapping']:
        dev = item['dev']

        (status, value) = lib.sensor.getValue(config, dev)
        
        aging = True

        if 'aging' in item:
            aging = item['aging']

        sensorId = item['id']

        if status == lib.sensor.VALUE_OK or ((not aging) and status == lib.sensor.VALUE_OLD):
            logValue(dev, value)
            sendValue(sensorId, value)

            print("%s %d %d" %(dev, sensorId, value))
            
