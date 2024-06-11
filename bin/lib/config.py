import yaml
import os

def read():
    return yaml.safe_load(open(os.environ.get('CONFIG')))
