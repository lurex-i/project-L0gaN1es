from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta
import pickle


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
    try:
        with open(filename, "wb") as f:
            execution_result = pickle.dump(book, f)
    except pickle.PicklingError:
        execution_result = "Could not save address book to file."
    except Exception as e:
        execution_result = f"Error has occured: {e}."
    return execution_result


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            execution_result = "Address book loaded successfully."
    except FileNotFoundError:
        book = AddressBook()
        execution_result = "File with address book not found.\nNew book created."
    except (pickle.UnpicklingError, EOFError):
        book = AddressBook()
        execution_result = "Could not load address book from file.\nNew book created."
    except Exception as e:
        book = AddressBook()
        execution_result = f"Error has occured: {e}.\nNew book created."
    return (book, execution_result)

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

def main():
    # Get book (loaded or new) and message from load_data
    book, execution_result = load_data()
    print("Welcome to the assistant bot!")
    # Warn user if we can't load book from file and use new one
    print(execution_result)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            # Try to save book before exit
            # If we can't save, print error message
            execution_result = save_data(book)
            if execution_result:
                print(execution_result)
            print("Good bye!")
            break
        elif command in commands.keys():
            print(commands[command](args, book))
            # Try to save book after each action
            # If we can't save, print error message
            execution_result = save_data(book)
            if execution_result:
                print(execution_result)
        else:
            print("Invalid command.")
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, exit/close")


if __name__ == "__main__":
     main()