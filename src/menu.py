import sys
import keyboard
from colorama import init, Fore, Style

class MenuItem():
    def __init__(self, key, name, help="", hint="", handler=None, next_level=None, error = ""):
        self.key = key
        self.name = name
        self.help = help
        self.hint = hint
        self.handler = handler
        self.next_level = next_level
        self.error = error


class MenuLevel():
    def __init__(self, name, items=[], show_info = None):
        self.name = name
        self.items = items
        self.show_info = show_info
        self.obj = None

    # when we start menu level
    def enter(self):
        print(self.name)
        if self.show_info:
            self.show_info(self.obj)
        for item in self.items:
            print(f"{item.key}. {item.name}   ", end='')
        print()
    
    @staticmethod
    def get_one_key():
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                return event.name
    
    @staticmethod
    def read_parameter() -> str:
        buffer = ""
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "enter":
                    # sys.stdout.write("\n")
                    # return cursor back for the hint lenght
                    sys.stdout.write(f"\x1b[{len(buffer)}D")
                    sys.stdout.flush()
                    break
                elif event.name == "space":
                    sys.stdout.write(" ")
                    # sys.stdout.flush()
                #todo - add esc combination 
                elif event.name == "esc":
                    raise Exception("Security! Cancelation!!!")
                # simple symbol like letter or number
                elif len(event.name) == 1:
                    buffer += event.name
                    # output symbol in default color to terminal
                    sys.stdout.write(event.name)
                    # sys.stdout.flush()
                # delete previous symbol
                elif event.name == "backspace" and buffer:
                    buffer = buffer[:-1]
                    # move cursor back and delete one symbol
                    sys.stdout.write("\x1b[1D \x1b[1D")
                    # sys.stdout.flush()
                sys.stdout.flush()
        return buffer

    def set_object(self, obj):
        self.obj = obj

    def make_step(self):
        while True:
            pressed = MenuLevel.get_one_key()
            if pressed in [x.key for x in self.items]:
                break
        # User select one of menu items. get object and run data input
        for item in self.items:
            if item.key == pressed:
                break

        if item.help:
            print(item.help)

        if item.hint:
            sys.stdout.write(Fore.LIGHTBLACK_EX + item.hint + Style.RESET_ALL)
            sys.stdout.flush()
            # return cursor back for the hint lenght
            sys.stdout.write(f"\x1b[{len(item.hint)}D")
            sys.stdout.flush()

        obj = None
        next = item.next_level
        if item.handler:
            try:
                buffer = MenuLevel.read_parameter()
                # Clear line from user input and our hint
                print(" " * max(len(item.hint), len(buffer)))
                message, obj = item.handler(buffer, self.obj)
            except:
                message, obj = (item.error, None)
                next = self
            print(message) # todo

        if obj and item.next_level:
            item.next_level.set_object(obj)

        return next
