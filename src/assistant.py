# Main script to launch assistant bot via CLI. 
# Uses Record and AddressBook classes directly
# Uses persistence.py for save/load operations

from record import Record
from address_book import AddressBook
from persistence import save_data, load_data
from note import Note
from colorama import init, Fore, Style
from menu import MenuItem, MenuLevel
from screensaver import random_image

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
def delete_contact(args, book:AddressBook):
    name, *_ = args
    record = book.find(name) 
    if record == None:
        return "There is no such contact in the address book."
    book.delete(name)
    return f"Contact for {name} was deleted."  

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
    name, *address = args
    address = " ".join(address)
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

@input_error
def add_note_cmd(args, book: AddressBook):
    text = " ".join(args)
    if not text.strip():
        raise ValueError("Note text cannot be empty.")
    note = Note(text)
    book.add_note(note)
    return "Note added."

@input_error
def add_tag_cmd(args, book: AddressBook):
    index = int(args[0])
    tag = args[1]

    if not tag.strip():
        raise ValueError("Tag cannot be empty.")
    if not (0 <= index < len(book.notes)):
        raise IndexError("Note index is out of range.")

    book.notes[index].add_tag(tag)
    return "Tag added."

@input_error
def del_note_cmd(args, book: AddressBook):
    if not args:
        raise IndexError("Enter note index after the command.")
    
    try:
        index = int(args[0])
    except ValueError:
        raise ValueError("Index must be a number.")

    book.delete_note(index)
    return "Note deleted."

@input_error
def find_note_cmd(args, book: AddressBook):
    keyword = " ".join(args)

    if not keyword.strip():
        raise ValueError("Search keyword cannot be empty.")

    results = book.find_notes_by_text(keyword)
    return "\n".join(str(n) for n in results) if results else "No notes found."

@input_error
def find_tag_cmd(args, book: AddressBook):
    tag = args[0]

    if not tag.strip():
        raise ValueError("Tag cannot be empty.")

    results = book.find_notes_by_tag(tag)
    return "\n".join(str(n) for n in results) if results else "No notes with such tag."

def show_notes_cmd(args, book: AddressBook):
    if not book.notes:
        return "No notes yet."
    return "\n".join(f"{i}: {note}" for i, note in enumerate(book.notes))

@input_error
def edit_note_cmd(args, book: AddressBook):
    if len(args) < 2:
        return "Give me index and new text please."
    
    index = int(args[0])
    new_text = " ".join(args[1:])
    
    book.edit_note_text(index, new_text)
    return f"Note {index} updated."

def sort_notes_cmd(args, book: AddressBook):
    return book.sort_notes_by_tags()

commands = {
    "hello": lambda args, book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "delete": delete_contact,
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
    print(random_image())
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
            print(random_image())
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
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays," \
            " add-note, show-note, add-tag, del-note, find-note, find-tag, edit-note, sort-notes," \
            "add-email, show-email, add-address, show-address, exit/close")


def add_record(name:str, book:AddressBook):
    # Check we have record
    record = book.find(name)
    if record:
        raise Exception("We already have contact with such name")
    record = Record(name)
    book.add_record(record)
    message = f"Contact {name} added"
    return (message, record)

def find_record(name:str, book:AddressBook):
    record = book.find(name)
    if not record:
        raise Exception(f"We don't have '{name}' contact")
    message = f"Contact '{record.name.value}' found"
    return (message, record)

def add_phone(name:str, record:Record):
    # todo
    return ("Phone added", record)

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

def show_book_info(book:AddressBook):
    print(f"has {len(book)} records and N notes") # todo - notes size

def show_record_info(record:Record):
    print(f"{record.name} [{record.phones}] born on {record.birthday}") # todo - colorama formated output


settings_menu = MenuLevel("Settings menu", [])
record_menu = MenuLevel("Record menu", [], show_record_info)
book_menu = MenuLevel("Address Book menu", [], show_book_info)

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
    print(random_image())
    menu = book_menu
    book_menu.set_object(book)
    while menu:
        menu.enter()
        menu = menu.make_step()

    save_data(book)
    print(random_image())
    print("Good bye!")


if __name__ == "__main__":
    main()
    # main_alt()
