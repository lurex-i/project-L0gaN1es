# Class for contact's phone number. Inherites Field class

from field import Field

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