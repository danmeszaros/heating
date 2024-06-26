import yaml
import os
import logging

def read():
    conf = yaml.safe_load(open(os.environ.get('CONFIG')))

    logging.basicConfig(filename=conf['logFile'], encoding='utf-8', level=logging.DEBUG)

    return conf
