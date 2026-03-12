from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta
import pickle

import sys
import keyboard
from colorama import init, Fore, Style


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    def __init__(self, value:str):
        if value and len(value) > 1:
            super().__init__(value.capitalize())
        else:
            raise Exception("Enter correct name for the contact")


class Phone(Field):
    def __init__(self, value:str):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if len(val) != 10 or not all(sym.isdigit() for sym in val):
            raise Exception("Phone number must be 10 digit format")
        self.__value = val


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise Exception("Invalid date format. Use DD.MM.YYYY")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val:date):
        year_now = datetime.now().date().year
        if val.year > year_now or val.year < year_now - 120:
            raise Exception("You made an error in the birthday's year.")
        self.__value = val
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday:str):
        self.birthday = Birthday(birthday)
    
    def add_phone(self, phone_num: str):
        if not phone_num in [phone.value for phone in self.phones]:
            self.phones.append(Phone(phone_num))

    def remove_phone(self, phone_num: str):
        self.phones.remove(self.find_phone(phone_num))

    def edit_phone(self, old_num, new_num):
        for index, phone in enumerate(self.phones):
            if phone.value == old_num:
                self.phones[index] = Phone(new_num)
                break

    def find_phone(self, phone_num: Phone):
        for phone in self.phones:
            if phone.value == phone_num:
                return phone
        return None


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name:str) -> Record:
        name = name.capitalize()
        if name in self.data.keys():
            return self.data[name]
        return None

    def delete(self, name:str):
        name = name.capitalize()
        del self.data[name]

    def get_upcoming_birthdays(self, days = 7):
        res_user_list = []
        now = datetime.today().date()
        for rec in self.data.values():
            if not rec.birthday.value:
                continue
            closest_bday = rec.birthday.value
            closest_bday = date.replace(closest_bday, year=now.year)
            # Check if birthday is in the past already and move it in the future
            if((closest_bday - now).days < 0):
                closest_bday = date.replace(closest_bday, year=now.year + 1)
            # Check birthday is next 7 days includes today
            if((closest_bday - now).days < days):
                #Correct congradulation day in case birthday is at weekend
                congr_day = closest_bday if closest_bday.weekday() < 5 else closest_bday + timedelta(days=7-closest_bday.weekday())
                res_user_list.append({"name":rec.name.value, 
                                      "congratulation_date":congr_day.strftime("%d.%m.%Y")})
        return res_user_list


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the correct argument for the command."
        except KeyError:
            return "There's no such user in the phonebook."
        except IndexError:
            return "Enter contact's name after the command."
        except Exception as e:
            return f"{e}"
    return inner



@input_error
def add_contact(args, book:AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated"
    if record == None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book:AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    if record == None:
        return "There is no such contact in the address book."
    record.edit_phone(phone, new_phone)
    return f"Contact for {name} was changed."

@input_error
def show_phone(args, book:AddressBook):
    name = args[0]
    name = name.capitalize()
    record = book.find(name)
    if record == None:
        return "There is no such contact in the address book."
    return f"{name} : {book[name]}."

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = ""
    if record == None:
        record = Record(name)
        book.add_record(record)
        message += "New contact was created. "
    record.add_birthday(birthday)
    message += f"Birthday at {record.birthday} for {name} was added."
    return message

@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record == None:
        return f"There is no {name} in the address book."
    return f"{name} : {record.birthday}"

@input_error
def birthdays(args, book:AddressBook):
    message = ""
    for day in book.get_upcoming_birthdays():
        message += f'Congratulate {day["name"]} on {day["congratulation_date"]}\n'
    if not message:
        message = "There are no upcoming bithdays next week"
    return message

def parse_input(user_input):
    if not user_input:
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def  show_all(args, book:AddressBook):
    message = ""
    for name, phone in book.items():
        message += f"{name} : {phone}\n"
    return message

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def greating():
    print("Welcome to the assistant bot!")

commands = {
    "hello": lambda args, book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "all":  show_all
}


# @input_error
def add_record(name:str, book:AddressBook):
    # Check we have record
    record = book.find(name)
    if record:
        raise Exception("We already have contact with such name")
    record = Record(name)
    book.add_record(record)
    message = "Contact added"
    return (message, record)

# @input_error
def find_record(name:str, book:AddressBook):
    record = book.find(name)
    if not record:
        raise Exception(f"We don't have '{name}' contact")
    message = f"Contact '{record.name.value}' found"
    return (message, record)

# @input_error
def add_phone(name:str, record:Record):
    # todo
    return ("Phone added", record)

# @input_error
def del_phone(name:str, record:Record):
    # todo
    return ("Phone deleted", record)

def get_birthdays(qnt:str, book:AddressBook):
    message = ""
    try:
        cl_days = int(qnt)
    except:
        cl_days = 7
        message += "It's not a number. I show birthdays for next week.\n"
    for day in book.get_upcoming_birthdays(cl_days):
        message += f'Congratulate {day["name"]} on {day["congratulation_date"]}\n'
    if not message:
        message = "There are no upcoming bithdays next week"
    return (message, None)


class MenuItem():
    def __init__(self, key, name, help="", hint="", handler=None, next_level=None):
        self.key = key
        self.name = name
        self.help = help
        self.hint = hint
        self.handler = handler
        self.next_level = next_level

    @staticmethod
    def get_one_key():
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                return event.name

    @staticmethod
    def select_item(items:list):
        buffer = ""

        while True:
            pressed = MenuItem.get_one_key()
            if pressed in [x.key for x in items]:
                break
        # User select one of menu items. get object and run data input
        for item in items:
            if item.key == pressed:
                break

        if item.hint:
            sys.stdout.write(Fore.LIGHTBLACK_EX + item.hint + Style.RESET_ALL)
            sys.stdout.flush()
            # return cursor back for the hint lenght
            sys.stdout.write(f"\x1b[{len(item.hint)}D")
            sys.stdout.flush()

        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "enter":
                    break
                elif event.name == "space":
                    sys.stdout.write(" ")
                    # sys.stdout.flush()
                #todo - add esc combination 
                elif event.name == "esc":
                    raise item.exception
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
        print()
        return item.handler(buffer)


class MenuLevel():
    def __init__(self, name, items=[]):
        self.name = name
        self.items = items
        self.obj = None

    # when we start menu level
    def enter(self):
        print(self.name)
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
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                elif event.name == "space":
                    sys.stdout.write(" ")
                    # sys.stdout.flush()
                #todo - add esc combination 
                elif event.name == "esc":
                    raise item.exception
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

        if item.hint:
            sys.stdout.write(Fore.LIGHTBLACK_EX + item.hint + Style.RESET_ALL)
            sys.stdout.flush()
            # return cursor back for the hint lenght
            sys.stdout.write(f"\x1b[{len(item.hint)}D")
            sys.stdout.flush()

        obj = None
        next = item.next_level
        if item.handler:
            buffer = MenuLevel.read_parameter()
            try:
                message, obj = item.handler(buffer, self.obj)
            except:
                message, obj = ("Make custom field with exception info", None)
                next = self
            print(message) # todo

        if obj and item.next_level:
            item.next_level.set_object(obj)

        return next



def main():
    book = load_data()
    greating()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command in commands.keys():
            print(commands[command](args, book))
        else:
            print("Invalid command.")
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, exit/close")
    save_data(book)


settings_menu = MenuLevel("Settings menu", [])
record_menu = MenuLevel("Record menu", [])
book_menu = MenuLevel("Address Book menu", [])

def init_menu():
    # Address book menu settings
    book_menu.items.append(MenuItem("1", "Add contact", "Enter contact name:", hint="John Snow", 
                                    handler=add_record, next_level=record_menu))
    book_menu.items.append(MenuItem("2", "Find contact", "Enter contact name:", hint="John Snow", 
                                    handler=find_record, next_level=record_menu))
    book_menu.items.append(MenuItem("3", "Find phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                    # handler=find_phone, 
                                    next_level=record_menu))
    book_menu.items.append(MenuItem("4", "Add note", "Enter tags;note text:", hint="tag1,tag2; Remember this!", 
                                    # handler=add_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("5", "Find note", "Enter tag/tags:", hint="tag1[,tag2]",
                                    # handler=find_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("7", "Closest birthdays", "How many days of the closest birthdays you want? ",
                                    handler=get_birthdays, next_level=book_menu))
    book_menu.items.append(MenuItem("8", "Settings", "",
                                    next_level=settings_menu))
    book_menu.items.append(MenuItem("0", "Exit"))
    # Record menu items
    record_menu.items.append(MenuItem("1", "Add phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                      handler=add_phone, next_level=record_menu))
    record_menu.items.append(MenuItem("2", "Del phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                      handler=del_phone, next_level=record_menu))
    record_menu.items.append(MenuItem("3", "Set address", "Enter home address:", 
                                    #   handler=set_address, 
                                      next_level=record_menu))
    record_menu.items.append(MenuItem("4", "Add mail", "Enter e-mail:", 
                                    #   handler=set_mail, 
                                      next_level=record_menu))
    record_menu.items.append(MenuItem("5", "Del mail", "What e-mail do you want delete? ", 
                                    #   handler=del_mail, 
                                      next_level=record_menu))
    record_menu.items.append(MenuItem("6", "Set birthday", "When he/she was born? ",  hint="DD.MM.YYYY",
                                    #   handler=set_birthday, 
                                      next_level=record_menu))
    record_menu.items.append(MenuItem("0", "Back", next_level=book_menu))
    # Settings menu items
    settings_menu.items.append(MenuItem("1", "Set family's tax: ", "Input average amount for a gift: ", 
                                    #   handler=set_family_tax, 
                                      next_level=settings_menu))
    settings_menu.items.append(MenuItem("2", "Set friend's tax: ", "Input average amount for a gift: ", 
                                    #   handler=set_friend_tax, 
                                      next_level=settings_menu))
    settings_menu.items.append(MenuItem("3", "Set colleague's tax: ", "Input average amount for a gift: ", 
                                    #   handler=set_colleague_tax, 
                                      next_level=settings_menu))
    settings_menu.items.append(MenuItem("0", "Back", next_level=book_menu))

def main_alt():
    book = load_data()
    init()
    init_menu()
    menu = book_menu
    while menu:
        menu.enter()
        menu = menu.make_step()

    print("Good bye!")


if __name__ == "__main__":
    # main()
    main_alt()


# Book - N records
# 1. Add    2. Find name   3. Find phone   4. Add note  5.Find note   7. Closest birthdays   9. Settings
# book.1.Add.Input.CallHandler.GoNextLev(input,obj)->MenuLevel(record)
# book.2.Find.Input.CallHandler.GoNextLev(input,obj)->MenuLevel(record)
# book.4.AddNote.InputTagNote.CallHandler.ReturnSameLevel->MenuLevel(book)
# book.5.FindNote.InputTag.CallHandler->outputNote.ReturnSameLevel->MenuLevel(book)
# book.7.ClosestB.InputDays.CallHandler->outputStats.ReturnSameLevel->MenuLevel(book)
# book.9.Settings.->GoSettingLevel->MenuLevel(settings)

# record.1.AddPhone.Input.CallHandler.SameLevel->MenuLevel(record)
# record.2.DelPhone.Input.CallHandler.SameLevel->MenuLevel(record)
# record.0.Back.GoUpperLev->MenuLevel(book)

# setting.1.Set relative tax.Input.CallHandler.SameLevel->MenuLevel(settings)
# setting.2.Set frien tax.Input.CallHandler.SameLevel->MenuLevel(settings)
# setting.0.Back.GoUpperLev->MenuLevel(book)

# Record - James Potter
# 1. Add phone  2. Del phone  2. Add Mail  4. Del mail  5. Set address    6. Set birthday     0. Back

