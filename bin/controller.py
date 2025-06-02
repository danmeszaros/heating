#!/usr/bin/python3

import lib.sensor
import lib.config
import pprint
import logging as log

#################################################################
# kolektorovy okruh
#
config = lib.config.read()

collectorTemp = lib.sensor.getValue(config, "temp3")[1]
collectorOutTemp = lib.sensor.getValue(config, "temp5")[1]

if collectorTemp > 45.0 or collectorOutTemp > 30.0:
    # turn on pump
    lib.sensor.setValue(config, "relay1", 1.0)
    log.info("starting collector pump")
elif collectorTemp < 20.0 or collectorOutTemp < 20.0:
    # turn off pump
    lib.sensor.setValue(config, "relay1", 0.0)
    log.info("stopping collector pump")
