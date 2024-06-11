# lib form manipulating sensor

import json
import tempfile
import time
import datetime
import os

def setValue(sensorName, value):

    if os.path.isfile(sensorName):
        sensorData = json.load(open(sensorName))

        history = sensorData['history']
        history.insert(0, {'value': sensorData['value'], 'ts': sensorData['ts'], 'datetime': sensorData['datetime']})

        if len(history) > 50:
            history = history[0:50]
    else:
        sensorData = {'history': []}

    

    sensorData['value'] = value
    sensorData['ts'] = int(time.time())
    sensorData['datetime'] = str(datetime.datetime.now()) # for debug only

    # write to tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(json.dumps(sensorData, indent=2, ensure_ascii=False,
                      sort_keys=False).encode("utf-8"))
        tmp.close()
        os.rename(tmp.name, sensorName)

        return True

    return False

