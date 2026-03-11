# Class for address book, stores all contacts as Records
# Inherites UserDict

from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta
from record import Record

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name:str) -> Record:
        name = name.capitalize()
        if name in self.data.keys():
            return self.data[name]
        return None

    def delete(self, name:str):
        name = name.capitalize()
        del self.data[name]

    def get_upcoming_birthdays(self):
        res_user_list = []
        now = datetime.today().date()
        for rec in self.data.values():
            if not rec.birthday.value:
                continue
            closest_bday = rec.birthday.value
            closest_bday = date.replace(closest_bday, year=now.year)
            # Check if birthday is in the past already and move it in the future
            if((closest_bday - now).days < 0):
                closest_bday = date.replace(closest_bday, year=now.year + 1)
            # Check birthday is next 7 days includes today
            if((closest_bday - now).days < 7):
                #Correct congradulation day in case birthday is at weekend
                congr_day = closest_bday if closest_bday.weekday() < 5 else closest_bday + timedelta(days=7-closest_bday.weekday())
                res_user_list.append({"name":rec.name.value, 
                                      "congratulation_date":congr_day.strftime("%d.%m.%Y")})
        return res_user_list