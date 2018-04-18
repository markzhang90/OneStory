import configparser
import os


def load_config(section, key, file="config.ini"):
    if section is None:
        return None
    cf = configparser.ConfigParser()
    file = os.path.dirname(os.path.realpath(__file__)) + '/' + file
    cf.read(file)
    try:
        if key is not None:
            res = cf.get(section, key)
        else:
            res = cf.options(section)
    except Exception:
        print("cant find ini")
        res = None
    return res
