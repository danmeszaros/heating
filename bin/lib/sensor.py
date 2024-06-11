# lib form manipulating sensor

import json
import tempfile
import time
import datetime
import os
import logging as log

VALUE_OK = 1
VALUE_OLD = 2
VALUE_ERROR = 3

VALUE_MAX_AGE = 300

def setValue(sensorName, value):

    try:
        if os.path.isfile(sensorName):
            sensorData = json.load(open(sensorName))

            history = sensorData['history']
            history.insert(0, {'value': sensorData['value'], 'ts': sensorData['ts'], 'datetime': sensorData['datetime']})

            if len(history) > 50:
                history = history[0:50]
        else:
            log.warning("creating file '%s'", sensorName)
            sensorData = {'history': []}
    except Exception as e:
        log.error("failed to init file '%s': %s", sensorName, repr(e))
        sensorData = {'history': []}


    try:
        sensorData['value'] = float(value)
        sensorData['ts'] = int(time.time())
        sensorData['datetime'] = str(datetime.datetime.now()) # for debug only

        # write to tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(json.dumps(sensorData, indent=2, ensure_ascii=False,
                          sort_keys=False).encode("utf-8"))
            tmp.close()
            os.rename(tmp.name, sensorName)

            return True
    except Exception as e:
        log.error("failed to write file '%s': %s", sensorName, repr(e))

    return False

def getValue(sensorName):
    try:
        sensorData = json.load(open(sensorName))
        # check value age
        nnow = time.time()

        if (nnow - sensorData['ts']) > VALUE_MAX_AGE:
            return (VALUE_OLD, sensorData['value'])

        return (VALUE_OK, sensorData['value'])
    except Exception as e:
        log.error("failed to read sensor '%s': %s", sensorName, repr(e))
        return (VALUE_ERROR, 0)
