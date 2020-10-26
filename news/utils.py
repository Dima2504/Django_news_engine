import time


def unique_slug():
    return str(time.time()).replace('.', '')
