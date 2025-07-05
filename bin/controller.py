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
boilerTemp = lib.sensor.getValue(config, "temp2")[1]
waterToGroundTemp = lib.sensor.getValue(config, "temp6")[1]
waterOutGroundTemp = lib.sensor.getValue(config, "temp7")[1]

"""
if collectorTemp > 45.0 or collectorOutTemp > 30.0:
    # turn on pump
    lib.sensor.setValue(config, "relay1", 1.0)
    log.info("starting collector pump")
elif collectorTemp < 20.0 or collectorOutTemp < 20.0:
    # turn off pump
    lib.sensor.setValue(config, "relay1", 0.0)
    log.info("stopping collector pump")
"""

#################################################################
# state machine
#
currentState = lib.sensor.getValue(config, "state0")[1]
newState = currentState
paused = False

if currentState == 0:
    # system off
    if collectorTemp > 45.0 or collectorOutTemp > 30.0:
        log.info("starting collector pump")
        newState = 1
elif currentState == 1:
    # ground circulation

    while True:
        # is the sytem stabilized?
        if lib.sensor.isValueStable(config, "state0", 10) == False:
            log.info("waiting for system to stabilize")
            # let system stabilize
            break

        if collectorTemp < 20.0 or collectorOutTemp < 20.0:
            log.info("system cool down, switching to 0")
            # it getting cold
            newState = 0
            break

        if waterToGroundTemp - waterOutGroundTemp < 2.0:
            log.info("ground gradient too low, switching to 0")
            newState = 0
            break

        # water to ground more than 18? enough power for heating the boiler
        if waterToGroundTemp > 18.0:
            log.info("switching to boiler")
            newState = 2
            break

        # no change
        break
    
elif currentState == 2:
    # boiler heating
    # of temp diff of boiler is smaller than 3
    # or if absolute temp of boiler 57C
    while True:
        # is the sytem stabilized?
        if lib.sensor.isValueStable(config, "state0", 10) == False:
            if lib.sensor.isValueStable(config, "state0", 5) == True:
                paused = True
                log.info("paused in state 2")
                break

            log.info("waiting for system to stabilize (state2)")
            # let system stabilize
            break

        if boilerTemp > 57:
            log.info("boiler temp on target. switching to 1")
            newState = 1
            break
        elif collectorOutTemp - boilerTemp < 3:
            # prevent cooling the boiler
            log.info("boiler heating temp not high enough, switching to 1")
            newState = 1
            break

        break
    


# update state
if currentState != newState:
    log.info("changing state from %d to %d" %(currentState, newState))

# update relays
if newState == 0:
    lib.sensor.setValue(config, "relay1", 0.0)
    lib.sensor.setValue(config, "relay8", 0.0)
    pass
elif newState == 1:
    lib.sensor.setValue(config, "relay1", 1.0)
    lib.sensor.setValue(config, "relay8", 0.0)
    pass
elif newState == 2:
    if paused:
        lib.sensor.setValue(config, "relay1", 0.0)
    else:
        lib.sensor.setValue(config, "relay1", 1.0)
    lib.sensor.setValue(config, "relay8", 1.0)
    pass

lib.sensor.setValue(config, "state0", newState)

