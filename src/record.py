# Separate class to store contact. It uses all field classes (Name, Phone, Birthday)

from name import Name
from phone import Phone
from birthday import Birthday

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