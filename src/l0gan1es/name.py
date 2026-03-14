# Class for contact's name. Inherites Field class

from field import Field

class Name(Field):
    # реалізація класу
    def __init__(self, value:str):
        if value and len(value) > 1:
            super().__init__(value) #.capitalize())
        else:
            raise Exception("Enter correct name for the contact")