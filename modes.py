from colorama import init, Fore, Back, Style
from random import randint, choice
import threading
import time
from shared import StopError, returnToMenu

init()

colorTable = {0: Back.BLACK,
              1: Back.RED,
              2: Back.GREEN,
              3: Back.YELLOW,
              4: Back.BLUE,
              5: Back.MAGENTA,
              6: Back.CYAN,
              7: Back.WHITE,
              }
def return_to_menu():
    print(Style.RESET_ALL)
    clear()

def check_stop():
    if threading.current_thread().stopped():
        print(Style.RESET_ALL)
        clear()
        raise StopError
def clear():
    print("\033[2J", end="") # Clear screen

def reset_cursor():
    print("\033[1;1H", end="")

def get_color(num):
    if num <= 7:
        return num
    else:
        return get_color(num-8)

def randomize_colors(colorTable):
    newOrder = []
    colors = [0, 1, 2, 3, 4, 5, 6, 7]
    while True:
        color = choice(colors)
        colors.remove(color)
        newOrder.append(color)
        if len(colors) == 0:
            break
    newColorTable = {0: False,
                     1: False,
                     2: False,
                     3: False,
                     4: False,
                     5: False,
                     6: False,
                     7: False,
                     }
    for a in range(8):
        newColorTable[a] = colorTable[newOrder[a]]
    return newColorTable

def color_fall(width, height):
    clear()
    newColorTable = randomize_colors(colorTable)
    while True:
        check_stop()
        if returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(height):
            color = get_color(a)
            print(newColorTable[color], end="")
            print(" " * width, end="")
            time.sleep(0.05)
        print(Back.RESET)
        clear()

def scan(width, height):
    clear()
    while True:
        check_stop()
        if returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(height-1): # -1 reset_cursor prints a line before moving
            if a % 2 == 0:
                color = get_color(randint(0, 7))
            print(colorTable[color], end="")
            print(" " * width, end="")
            time.sleep(0.05)
        reset_cursor()

def wave(width, height, modifier="normal"):
    clear()
    newColorTable = randomize_colors(colorTable)
    columns = 0
    if modifier == "default":
        change = 1
    elif modifier == "inverted":
        change = -1
    while True:
        check_stop()
        if returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(int(round((width+change)/2))):
            color = (a % 8)
            print(newColorTable[color], end="")
            print(" "*2, end="")
        columns += 1
        if columns > height:
            time.sleep(0.02)

def ripple(width, height, length=8):
    clear()
    newColorTable = randomize_colors(colorTable)
    columns = 0
    change = 1
    while True:
        check_stop()
        if returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(length):
            for a in range(int(round((width+change)/2))):
                color = (a % 8)
                print(newColorTable[color], end="")
                print(" "*2, end="")
            if columns > height:
                time.sleep(length/1000)
            columns += 1
        change = -change
