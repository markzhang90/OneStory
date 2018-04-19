import time


def decorator(func):
    def wrapper(*args, **kwargs):
        print("time checker start")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)
    return wrapper