# Main script to launch assistant bot via CLI. 
# Uses Record and AddressBook classes directly
# Uses persistence.py for save/load operations

from record import Record
from address_book import AddressBook
from persistence import save_data, load_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{e}"
        except ValueError:
            return "Enter the correct argument for the command."
        except KeyError:
            return "There's no such user in the phonebook."
        except IndexError:
            return "Enter contact's name after the command." 
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
def add_email(args, book:AddressBook):
    name, email, *_ = args
    record = book.find(name)
    message = ""
    if record == None:
        record = Record(name)
        book.add_record(record)
        message += "New contact was created. "
    record.add_email(email)
    message += f"Email at {record.email} for {name} was added."
    return message

@input_error
def show_email(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record == None:
        return f"There is no {name} in the address book."
    return f"{name} : {record.email}"

@input_error
def add_address(args, book:AddressBook):
    name, address, *_ = args
    record = book.find(name)
    message = ""
    if record == None:
        record = Record(name)
        book.add_record(record)
        message += "New contact was created. "
    record.add_address(address)
    message += f"Address at {record.address} for {name} was added."
    return message

@input_error
def show_address(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record == None:
        return f"There is no {name} in the address book."
    return f"{name} : {record.address}" 

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

commands = {
    "hello": lambda args, book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "add-email": add_email,
    "show-email": show_email,
    "add-address": add_address,
    "show-address": show_address,
    "all": show_all
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
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, add-email, show-email, add-address, show-address, exit/close")


if __name__ == "__main__":
     main()