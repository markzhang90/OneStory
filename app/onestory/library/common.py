import time
import json


def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("time checker start " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
        func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)
    return wrapper


def json_out(input_arr):
    try:
        if type(input_arr) is dict or type(input_arr) is list:
            return json.dumps(input_arr)
        return str(input_arr)
    except ValueError:
        return input_arr
