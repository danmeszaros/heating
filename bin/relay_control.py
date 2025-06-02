#!/usr/bin/python3

import logging as log
import http.client
import datetime
import lib.sensor
import lib.config
import subprocess

def logValue(sensorId, value):
    fname = config['appRoot'] + config['reporter']['valueLog']

    try:
        outf = open(fname, "a")
        outf.write(str(datetime.datetime.now()) + " ")
        outf.write("%s %.1f" %(sensorId, value) + "\n")
        outf.close()
    except Exception as e:
        log.error("failed to write to log '%s': %s", fname, repr(e))

def setRelay(relay_id, value):
    try:
        print("executing usbrelay A_%d=%d" %(relay_id, value))
        subprocess.run(["usbrelay", "A_%d=%d" %(relay_id, value)])
    except:
        log.error("failed to execute usbrelay MRB1O_%d" %relay_id)
        pass

if __name__ == "__main__":
    config = lib.config.read()

    for item in config['reporter']['mapping']:
        dev = item['dev']

        if dev[0:5] != "relay":
            continue

        (status, value) = lib.sensor.getValue(config, dev)
        
        relayId = int(dev[5:])
        setRelay(relayId, value)

        print("%s %d" %(dev, value))
            
