# Main script to launch assistant bot via CLI. 
# Uses Record and AddressBook classes directly
# Uses persistence.py for save/load operations

from record import Record
from address_book import AddressBook
from persistence import save_data, load_data
from note import Note
from colorama import init, Fore, Style
from menu import MenuItem, MenuLevel
import random
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
    period = args[0] if args else "7"
    for day in book.get_upcoming_birthdays(period):
        message += f'Congratulate {day["name"]} on {day["congratulation_date"]}\n'
    if not message:
        message = f"There are no upcoming bithdays in the next {period} days."
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
    colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.MAGENTA]  
    for name, phone in book.items():
        record = (random.choice(colors) + f"{name} : {phone}\n" + Style.RESET_ALL) 
        message += record  
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
    "add-note": add_note_cmd,
    "show-notes": show_notes_cmd,
    "add-tag": add_tag_cmd,
    "del-note": del_note_cmd,
    "find-note": find_note_cmd,
    "find-tag": find_tag_cmd,
    "edit-note": edit_note_cmd,
    "sort-notes": sort_notes_cmd,
    "add-email": add_email,
    "show-email": show_email,
    "add-address": add_address,
    "show-address": show_address, 
    "all": show_all 
}


def add_record(name:str, book:AddressBook):
    # Check we have record
    record = book.find(name)
    if record:
        raise Exception("We already have contact with such name")
    record = Record(name)
    book.add_record(record)
    message = f"Contact {name} added"
    return (message, record)

def delete_record(name:str, book:AddressBook):
    record = book.find(name)
    if record == None:
        return ("We don't have contact with such name", book)
    book.delete(name)
    message = f"Contact {name} deleted"
    return (message, book)

def find_record(name:str, book:AddressBook):
    record = book.find(name)
    if not record:
        raise Exception(f"We don't have '{name}' contact")
        # return (f"We don't have '{name}' contact", None)
    message = f"Contact '{record.name}' found"
    return (message, record)

# Look into all contacts for specific phone number and return massege ane record object
def find_phone(number:str, book:AddressBook):
    for rec in book.values():
        if rec.find_phone(number):
            return (f"Phone number {number} found in {rec.name}", rec)
    return (f"We don't have {number} phone number", None)

def add_phone(number:str, record:Record):
    record.add_phone(number)
    return (f"Phone {number} added", record)

def del_phone(number:str, record:Record):
    record.remove_phone(number)
    return (f"Phone {number} deleted", record)

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
        message = f"There are no upcoming bithdays next {cl_days} days"
    return (message, None)

def add_note(text:str, book: AddressBook):
    if not text.strip():
        return ("Note text cannot be empty.", book)
    book.add_note(Note(text))
    return ("Note added.", book)

def add_tag(tag:str, book: AddressBook):
    index, *tags = tag.split()
    index = int(index)
    if len(tags) == 0:
        return ("Tag cannot be empty.", book)
    if not (0 <= index < len(book.notes)):
        return ("Note index is out of range.", book)
    for t in tags:
        book.notes[index].add_tag(t)
    return ("Tag added.", book)

def del_note(index:str, book: AddressBook):
    if not index:
        return ("Enter note index after the command.", book)
    try:
        index = int(index)
    except ValueError:
        return ("Index must be a number.", book)
    book.delete_note(index)
    return ("Note deleted.", book)

def find_note(keyword, book: AddressBook):
    if not keyword.strip():
        return ("Search keyword cannot be empty.", book)
    results = book.find_notes_by_text(keyword)
    message = "\n".join(str(n) for n in results) if results else "No notes found."
    return (message, book)

def find_tag(tag, book: AddressBook):
    if not tag.strip():
        return ("Tag cannot be empty.", book)
    results = book.find_notes_by_tag(tag)
    message = "\n".join(str(n) for n in results) if results else "No notes with such tag."
    return (message, book)

def show_notes(text, book: AddressBook):
    if not book.notes:
        return ("No notes yet.", book)
    message = "\n".join(f"{i}: {note}" for i, note in enumerate(book.notes))
    return (message, book)

def edit_note(text:str, book: AddressBook):
    index, *note_body = text.split()
    try:
        i = int(index)
    except:
        return ("Index must be a number.", book)
    new_text = " ".join(note_body)
    book.edit_note_text(index, new_text)
    return (f"Note {index} updated.", book)


def add_email_item(email, record: Record):
    record.add_email(email)
    return (f"Email at {record.email} for {record.name} was added.", record)

def set_address(addr:str, record: Record):   
    record.add_address(addr)
    return (f"Address at {record.address} for {record.name} was added.", record)

def set_birthday(birthday:str, record: Record):
    record.add_birthday(birthday)
    return (f"Birthday at {record.birthday} for {name} was added.", record)


def  show_book(none:str, book:AddressBook):
    message = "" 
    for name, phone in book.items():
        message += f"{phone}\n"
    print() 
    return (message, book)

def show_book_info(book:AddressBook):
    print(f"has {len(book)} records and {len(book.notes)} notes")

def show_record_info(record:Record):
    colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.MAGENTA]
    # print(f"{record}") # short version by __str__
    print(random.choice(colors) + f"{record}" + Style.RESET_ALL)  


settings_menu = MenuLevel("Settings menu", [])
record_menu = MenuLevel("Record menu", [], show_record_info)
book_menu = MenuLevel("Address Book menu", [], show_book_info)
exit_menu = MenuLevel("", [])

def init_menu():
    # Address book menu settings
    book_menu.items.append(MenuItem("1", "Add contact", "Enter contact name:", hint="John Snow", 
                                    handler=add_record, next_level=record_menu))
    book_menu.items.append(MenuItem("2", "Find contact", "Enter contact name:", hint="John Snow", 
                                    handler=find_record, next_level=record_menu, error="We don't have such contact"))
    book_menu.items.append(MenuItem("3", "Find phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                    handler=find_phone,
                                    next_level=record_menu))
    book_menu.items.append(MenuItem("4", "Add note", "Enter note text:",
                                    handler=add_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("5", "Find note", "Enter keyword from note:", #"Enter tag/tags:", #hint="tag1[,tag2]",
                                    handler=find_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("6", "Edit note", "Enter index and new note:", hint="2 Buy red ferrari.",
                                    handler=edit_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("7", "Del note", "Enter note's index to delete:",
                                    handler=del_note, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("8", "Closest birthdays", "How many days of the closest birthdays you want? ",
                                    handler=get_birthdays, next_level=book_menu))
    book_menu.items.append(MenuItem("9", "Show all", "", 
                                    handler=show_book, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("0", "Exit"))
    book_menu.items.append(MenuItem("D", "Del contact", "Enter contact to delete:",
                                    handler=delete_record,
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("t", "Add tag", "Enter index and tags:", hint="1 tag1 tag2", 
                                    handler=add_tag, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("f", "Find tag", "Enter tag to find:", hint="tag", 
                                    handler=find_tag, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("n", "Show notes", "", #hint="tag", 
                                    handler=show_notes, 
                                    next_level=book_menu))
    book_menu.items.append(MenuItem("c", "Command style", "", #hint="tag", 
                                    # handler=show_notes, 
                                    next_level=exit_menu))
    # book_menu.items.append(MenuItem("8", "Settings", "",
    #                                 next_level=settings_menu))

    # Record menu items
    record_menu.items.append(MenuItem("1", "Add phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                      handler=add_phone, next_level=record_menu))
    record_menu.items.append(MenuItem("2", "Del phone", "Enter phone number:", hint="0xxxxxxxxx", 
                                      handler=del_phone, next_level=record_menu))
    record_menu.items.append(MenuItem("3", "Set address", "Enter home address:", 
                                      handler=set_address, 
                                      next_level=record_menu))
    record_menu.items.append(MenuItem("4", "Add mail", "Enter e-mail:", 
                                      handler=add_email_item, 
                                      next_level=record_menu))
    # record_menu.items.append(MenuItem("5", "Del mail", "What e-mail do you want delete? ", 
    #                                   handler=del_mail_item, 
    #                                   next_level=record_menu))
    record_menu.items.append(MenuItem("5", "Set birthday", "When he/she was born? ",  hint="DD.MM.YYYY",
                                      handler=set_birthday, 
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

def operate_command(book):
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            return 0
        elif command == "menu":
            return 1

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
            "add-email, show-email, add-address, show-address, menu, exit/close")

def operate_menu(book):
    init()
    init_menu()
    menu = book_menu
    book_menu.set_object(book)
    while menu:
        menu.enter()
        menu = menu.make_step()
        if menu == exit_menu:
            return 2
    return 0

def main():
    # Get book (loaded or new) and message from load_data
    book, execution_result = load_data()
    print(random_image())
    print("Welcome to the assistant bot!")
    # Warn user if we can't load book from file and use new one
    print(execution_result)

    mode = 1
    while mode:
        if mode == 1:
            mode = operate_menu(book)
        if mode == 2:
            mode = operate_command(book) 

    execution_result = save_data(book)
    print(random_image())
    if execution_result:
        print(execution_result)
    print("Good bye!")


if __name__ == "__main__":
    main()
