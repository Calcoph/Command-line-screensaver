import threading

class StopError(Exception):
    pass

returnToMenu = threading.Event()
end_calibration = threading.Event()
increase_bar = threading.Event()
decrease_bar = threading.Event()
increase_speed = threading.Event()
decrease_speed = threading.Event()
