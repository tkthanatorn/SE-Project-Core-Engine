from yaml import safe_load, YAMLError
import os

CONFIG_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml"))


def get_config(keys=[]):
    # config variable
    configs = dict()

    # read config file
    with open(CONFIG_PATH, 'r') as stream:
        try:
            configs = safe_load(stream)
        except YAMLError as e:
            print(e)
    
    for key in keys:
        configs = configs[key]
    
    return configs
    
