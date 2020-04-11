from colorama import init, Cursor, Back
import modes
import multiprocessing as mp
import threading
import json
import shared
import time

init()

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, target=None):
        super(StoppableThread, self).__init__(target=target)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
def create_profile():
    shared.end_calibration.clear()
    print("\033[2J", end="") # clear screen
    def print_bar(size):
        print(Back.GREEN, end="")
        print(" " * size, end="")
        print(Back.RESET, end="")
        time.sleep(0.1)
        print("\033[f") # Move to upper left corner
        #print("\033[1B") # Move down 1 line
        print("\033[J", end="") # Erase screen from cursor down
        #print("\033[2K", end="") # Erases the line
    width = 100
    print("Move the bar with A and D until it fits exactly one row of the console, press G when it's ready")
    while True:
        print_bar(width)
        if shared.increase_bar.is_set():
            shared.increase_bar.clear()
            width += 1
        if shared.decrease_bar.is_set():
            shared.decrease_bar.clear()
            width -= 1
        if shared.end_calibration.is_set():
            shared.end_calibration.clear()
            break
    
    print("\033[2J", end="") # clear screen
    for i in range(100):
        print(i)
    height = int(input("If you scroll so 0 is at the top of the console, what is the last number you see?"))
    print(f"Your console is {width}x{height}")

    name = input("Name this profile: ")

    with open("profiles.json", "r") as f:
        profiles = json.loads(f.read())

    profiles[name] = {
            "width": width,
            "height": height
        }
    json_profiles = json.dumps(profiles)

    with open("profiles.json", "w") as f:
        f.write(json_profiles)

def delete_profile():
    with open("profiles.json", "r") as f:
        profiles = json.loads(f.read())
    options = "What profile do you want to delete? "
    enumeration = enumerate(profiles)
    for i in profiles:
        options += f"{i}"
    
    answer = input(options)
    del profiles[answer]

    json_profiles = json.dumps(profiles)
    with open("profiles.json", "w") as f:
        f.write(json_profiles)

def check_stop():
    if threading.current_thread().stopped():
        raise shared.StopError

def main():
    try:
        profiles = None
        with open("profiles.json", "r") as f:
            profiles = json.loads(f.read())
                
        
        def ask_again():
            print("\033[1A", end="") # Moves cursor up
            print("\033[2K", end="") # Erases the line

        def check_input(inp): # !!!!!!!    WIP    !!!!!!!!
            check_stop()
            options = []

            for index, i in enumerate(profiles):
                options.append(str(index))
            if inp.isdigit and inp in options:
                return int(inp)
            elif inp == "config":
                return inp
            else:
                ask_again()
                inp = ask()
                return inp

        def ask():
            string = ""
            for index, i in enumerate(profiles):
                string += f"{index}: {i}, "
            string = string[:-2] + ": "
            answer = check_input(input(string))
            return answer
        def config():
            answer = input("what do you want to do? 0: create new profile, 1: delete profile")
            if answer == "0":
                create_profile()
            elif answer == "1":
                delete_profile()
            elif answer == "2":
                change_order()
            else:
                print("That's not an available option! type 0, 1 or 2")
                config()

        print()
        print('Welcome to the command line screen saver! press "x" at any time \
to exit the program or m to return to the menu. Type config to manage profiles')
        answer = ask()

        if answer == "config":
            config()
        else:
            draw(answer, profiles)
    except shared.StopError:
        pass
def draw(option, profiles):
    try:
        height = 0
        width = 0
        for index, i in enumerate(profiles):
            if option == index:
                width = profiles[i]["width"]
                height = profiles[i]["height"]

        def manage_mode_input(inp):
            check_stop()
            if inp.isdigit() and inp in ["0", "1", "2", "3"]:
                return int(inp)

            elif inp.isdigit():
                ask_again()
                return manage_mode_input(input("Choose mode: "))

            else:
                inp = inp.lower()
                mode_conversion = {
                    ("color fall", "color_fall", "c"): 0,
                    ("scan", "scanner", "scaner", "s"): 1,
                    ("wave", "color wave", "color_wave", "w"): 2,
                    ("ripple", "rip", "r"): 3
                }

                for spell_list in mode_conversion:
                    for spelling in spell_list:
                        if inp == spelling:
                            return mode_conversion[spell_list]
                ask_again()
                return manage_mode_input(input("Choose mode: "))

        def manage_modifier_input(inp, mode):
            check_stop()
            inp = inp.lower()
            def isblank(input):
                inp = list(input)
                for a in inp:
                    if a != " ":
                        return False
                return True
            if mode == 2:
                modifier_conversion = {
                    ("","0", "normal"): "default",
                    ("1", "reverse"): "inverted"
                }
                for spell_list in modifier_conversion:
                    for spelling in spell_list:
                        if inp == spelling:
                            return modifier_conversion[spell_list]
                if isblank(inp):
                    return "default"
                ask_again()
                return manage_modifier_input(input("Choose modifier"\
                                                    + "(leave blank for default): "
                                                    ), 2)
            if mode == 3:
                if isblank(inp):
                    return 8
                if inp.isdigit:
                    if int(inp) >= 100:
                        return 100
                    elif int(inp) <= 0:
                        return 1
                    else:
                        return int(inp)
                else:
                    ask_again()
                    return manage_modifier_input(input("Choose length of ripples"\
                                                    + "(leave blank for default):"
                                                    ), 3)

        while True:
            print("Modes: color fall(0) | scan(1) | wave(2) | ripple(3)")
            print("Press J and N to change the speed once the mode is selected")
            mode = manage_mode_input(input("choose mode: "))
            if shared.returnToMenu.is_set():
                shared.returnToMenu.clear()
            if mode == 0:
                modes.color_fall(width, height)
            elif mode == 1:
                modes.scan(width, height)
            elif mode == 2:
                print("")
                print("Modifiers: default(0) | inverted (1)")
                modifier = manage_modifier_input(input("Choose modifier"\
                                                       + "(leave blank for default):"
                                                       ), 2)
                modes.wave(width, height, modifier)
            elif mode == 3:
                print("")
                length = manage_modifier_input(input("Choose length of ripples"\
                                                       + "(leave blank for default):"
                                                       ), 3)
                modes.ripple(width, height, length)
    except shared.StopError:
        pass

main_t = StoppableThread(target=main)
main_t.start()



import hotkeys
