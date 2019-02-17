from pynput import keyboard
from colorama import Style, init
import threading
import sys
import time
from shared import returnToMenu

init()

if __name__ == "__main__":
    exit()

def return_to_menu():
    returnToMenu.set()
def safely_exit():
    threading.enumerate()[1].stop()
    time.sleep(0.5)
    sys.exit()

def on_press(key):
    if key == keyboard.KeyCode(char="x"):
        safely_exit()
    if key == keyboard.KeyCode(char="m"):
        return_to_menu()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
