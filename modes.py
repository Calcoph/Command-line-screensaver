from colorama import init, Fore, Back, Style
from random import randint, choice
import threading
import time
import shared

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
        raise shared.StopError
def clear():
    print("\033[2J", end="") # Clear screen

def reset_cursor():
    print("\033[1;1H", end="")

def get_color(num):
    if num <= 7:
        return num
    else:
        return get_color(num-8)

def check_speed():
    if shared.decrease_speed.is_set():
        speed_change = -0.01
        shared.decrease_speed.clear()
    elif shared.increase_speed.is_set():
        speed_change = 0.01
        shared.increase_speed.clear()
    else:
        speed_change = 0
    return speed_change

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
    time_gap = 0.05
    while True:
        check_stop()
        if shared.returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(height):
            color = get_color(a)
            print(newColorTable[color], end="")
            print(" " * width, end="")
            time_gap += check_speed()
            if time_gap < 0:
                time_gap = 0
            time.sleep(time_gap)
        print(Back.RESET)
        clear()

def scan(width, height):
    clear()
    time_gap = 0.05
    while True:
        check_stop()
        if shared.returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(height-1): # -1 reset_cursor prints a line before moving
            if a % 2 == 0:
                color = get_color(randint(0, 7))
            print(colorTable[color], end="")
            print(" " * width, end="")
            time_gap += check_speed()
            if time_gap < 0:
                time_gap = 0
            time.sleep(time_gap)
        reset_cursor()

def wave(width, height, modifier="default"):
    clear()
    newColorTable = randomize_colors(colorTable)
    columns = 0
    if modifier == "default":
        change = 2
    elif modifier == "inverted":
        change = -2
    
    time_gap = 0.02
    while True:
        check_stop()
        if shared.returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(width+change):
            color = int((a % 32)/4)
            print(newColorTable[color], end="")
            print(" ", end="")
        columns += 1
        if columns > height:
            columns = height
            time_gap += check_speed()
            if time_gap < 0:
                time_gap = 0
            time.sleep(time_gap)

def ripple(width, height, length=8):
    clear()
    newColorTable = randomize_colors(colorTable)
    columns = 0
    change = 2
    time_gap = length/1000
    while True:
        check_stop()
        if shared.returnToMenu.is_set():
            return_to_menu()
            break
        for a in range(length):
            for a in range(width+change):
                color = int((a % 32)/4)
                print(newColorTable[color], end="")
                print(" ", end="")
            if columns > height:
                columns = height
                time_gap += check_speed()
                if time_gap < 0:
                    time_gap = 0
                time.sleep(time_gap)
            columns += 1
        change = -change
