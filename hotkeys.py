from pynput import keyboard
from colorama import Style, init
import threading
import sys
import time
import shared

init()

if __name__ == "__main__":
    exit()

def safely_exit():
    threading.enumerate()[1].stop()
    time.sleep(0.5)
    sys.exit()

def on_press(key):
    if key == keyboard.KeyCode(char="x"):
        safely_exit()
    if key == keyboard.KeyCode(char="m"):
        shared.returnToMenu.set()
    if key == keyboard.KeyCode(char="g"):
        shared.end_calibration.set()
    if key == keyboard.KeyCode(char="a"):
        shared.decrease_bar.set()
    if key == keyboard.KeyCode(char="d"):
        shared.increase_bar.set()
    if key == keyboard.KeyCode(char="j"):
        shared.decrease_speed.set()
    if key == keyboard.KeyCode(char="n"):
        shared.increase_speed.set()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
