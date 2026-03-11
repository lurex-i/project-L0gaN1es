from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta
import pickle

import sys
import keyboard
from colorama import init, Fore, Style
from typing import List


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

    def get_upcoming_birthdays(self):
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
            if((closest_bday - now).days < 7):
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



class MenuItem():
    def __init__(self, key, name, input_text, hint, handler, exception):
        self.key = key
        self.name = name
        self.input_text = input_text
        self.hint = hint
        self.handler = handler
        self.exception = exception

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



def get_input_hint(hint:str):
    buffer = ""
    sys.stdout.write(Fore.LIGHTBLACK_EX + hint + Style.RESET_ALL)
    sys.stdout.flush()
    # return cursor back for the hint lenght
    sys.stdout.write(f"\x1b[{len(hint)}D")
    sys.stdout.flush()

    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "enter":
                break
            elif event.name == "space":
                sys.stdout.write(" ")
            #todo - add esc combination 

            # simple symbol like letter or number
            elif len(event.name) == 1:
                buffer += event.name
                # output symbol in default color to terminal
                sys.stdout.write(event.name)
                sys.stdout.flush()
            # delete previous symbol
            elif event.name == "backspace" and buffer:
                buffer = buffer[:-1]
                # move cursor back and delete one symbol
                sys.stdout.write("\x1b[1D \x1b[1D")
                sys.stdout.flush()

    return buffer


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


menu_items = [ 
    MenuItem("1", "Add contact", 
             input_text="Enter contact name:",
             hint="John Snow", 
             handler=lambda _:"dummy", 
             exception=Exception("custom exception")), 
    MenuItem("2", "Find contact", 
             input_text="Enter contact name:",
             hint="Harry Potter", 
             handler = lambda x:print(f"**{x}**"), 
             exception=Exception("custom exception")),
    MenuItem("3", "Add note", 
             input_text="Input your note. At the end press Enter twice",
             hint="", 
             handler=lambda _:"dummy", 
             exception=Exception("custom exception")),
    MenuItem("4", "Find note", 
             input_text="Input notes tag you are looking for:",
             hint="", 
             handler=lambda _:"dummy", 
             exception=Exception("custom exception"))]


def main_alt():
    init()
    for item in menu_items:
        print(f"{item.key}. {item.name}   ", end='')
    print()
    # inp = get_input_hint()
    MenuItem.select_item(menu_items)

    # get_input_hint("(0xx)-xxx-xx-xx")
    # get_input_hint("Name Surname")
    # get_input_hint("YYYY.MM.DD")

if __name__ == "__main__":
    # main()
    main_alt()