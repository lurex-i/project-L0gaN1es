# Main script to launch assistant bot via CLI. 
# Uses Record and AddressBook classes directly
# Uses persistence.py for save/load operations

from record import Record
from address_book import AddressBook
from persistence import save_data, load_data
from note import Note

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)  
        except ValueError:
            return "Enter the correct argument for the command."
        except KeyError:
            return "There's no such user in the phonebook."
<<<<<<< feature/note/tag
        except IndexError as i:
            return str(i) if str(i) else "Missing or invalid index."
=======
        except IndexError:
            return "Enter contact's name after the command." 
>>>>>>> main
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
<<<<<<< feature/note/tag
    "all":  show_all,
    "add-note": add_note_cmd,
    "show-notes": show_notes_cmd,
    "add-tag": add_tag_cmd,
    "del-note": del_note_cmd,
    "find-note": find_note_cmd,
    "find-tag": find_tag_cmd,
    "edit-note": edit_note_cmd,
    "sort-notes": sort_notes_cmd
=======
    "add-email": add_email,
    "show-email": show_email,
    "add-address": add_address,
    "show-address": show_address, 
    "all": show_all 
>>>>>>> main
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
<<<<<<< feature/note/tag
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays," \
            " add-note, show-note, add-tag, del-note, find-note, find-tag, edit-note, sort-notes, exit/close")
=======
            print("Use one of: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, add-email, show-email, add-address, show-address, exit/close")
>>>>>>> main


if __name__ == "__main__":
     main()
