from src.constant import LOGO_PATH
import os
from datetime import datetime


def LogHeader():
    with open(os.path.abspath(LOGO_PATH), 'r') as logo:
        print(logo.read())
        logo.close()


def Log(cname: str):
    def inner(function):
        def wrapper(*args, **kwargs):
            now = datetime.now()
            fname = function.__name__
            print(
                f"time: {now.date()} {now.hour}:{now.minute}:{now.second}, class: {cname}, function: {fname}()")
            result = function(*args, **kwargs)
            return result
        return wrapper
    return inner
