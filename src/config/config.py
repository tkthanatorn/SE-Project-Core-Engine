from typing import List
from yaml import safe_load, YAMLError
from src.constant import CONFIG_PATH
import os


def get_config(names=[]):
    # config variable
    configs = dict()

    # read config file
    with open(os.path.abspath(CONFIG_PATH), 'r') as stream:
        try:
            configs = safe_load(stream)
        except YAMLError as err:
            print(err)

    # filter config by names
    for key in names:
        configs = configs[key]

    return configs
