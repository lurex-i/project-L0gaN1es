# Separate class to store contact. It uses all field classes (Name, Phone, Birthday)

from name import Name
from phone import Phone
from birthday import Birthday
from email_address import EmailAddress  
from address import Address

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday:str):
        self.birthday = Birthday(birthday)

    def add_email(self, email:str):
        self.email = EmailAddress(email)

    def add_address(self, address:str):
        self.address = Address(address)
    
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
    
    def query_match(self, query: str) -> bool:
        query = query.lower()

        # Get all phone numbers as strings from phones
        phone_values = [phone.value for phone in self.phones]

        # Prepare string representations for each required field
        str_reps = [
            self.name.value.lower(),
            self.email.value.lower() if self.email else "",
            str(self.birthday) if self.birthday else ""
        ] + phone_values
        
        return any(query in rep for rep in str_reps)

    if __name__ == "__main__":
        address1 = Address("app65, str. Main")
        address2 = Address(" ")
        print(address1)
        print(address2)