# Contains functions for file operations (save/load) and corresponding error handling

import pickle
from address_book import AddressBook

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