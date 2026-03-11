# Class for contact's birthday. Inherites Field class

from datetime import datetime
from datetime import date
from field import Field

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