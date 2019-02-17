import threading

class StopError(Exception):
    pass

returnToMenu = threading.Event()
