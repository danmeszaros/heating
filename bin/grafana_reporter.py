#!/usr/bin/python3

import logging as log
import http.client
import datetime
import lib.sensor
import lib.config

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
            print("%s %d %d" %(dev, sensorId, value))
            
