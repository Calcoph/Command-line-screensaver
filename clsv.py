from colorama import init, Cursor
import modes
import multiprocessing as mp
import threading
from shared import StopError, returnToMenu

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

def main():
    try:
        def check_stop():
            if threading.current_thread().stopped():
                raise StopError
        def ask_again():
            print("\033[1A", end="") # Moves cursor up
            print("\033[2K", end="") # Erases the line

        def check_input(inp): # !!!!!!!    WIP    !!!!!!!!
            check_stop()
            if inp.isdigit and inp in ["0", "1", "2"]:
                return int(inp)
            else:
                ask_again()
                inp = check_input(input(
                                        "0: atom terminal, 1: 1920x1080, 2: 1440x900: "
                                        )
                                  )
                return inp
        print()
        print("""Welcome to the command line screen saver! press "x" at any time\
 to exit the program or m to return to the menu.""")
        resolution = check_input(input(
                                       "0: atom terminal, 1: 1920x1080, 2: 1440x900: "
                                       )
                                 )

        height = 0
        width = 0

        if resolution == 0:
            height = 14
            width = 194
        elif resolution == 1:
            height = 72
            width = 271
        elif resolution == 2:
            height = 61
            width = 203
        else:
            print("I don't know what you did but don't do it again")

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
            mode = manage_mode_input(input("choose mode: "))
            if returnToMenu.is_set():
                returnToMenu.clear()
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
    except StopError:
        pass

main_t = StoppableThread(target=main)
main_t.start()



import hotkeys
