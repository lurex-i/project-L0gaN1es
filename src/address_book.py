# Class for address book, stores all contacts as Records
# Inherites UserDict

from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta
from record import Record
from note import Note

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notes: list[Note] = []   

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
    
    def add_note(self, note: Note):
        if not note.text.strip():
            raise ValueError("Note text cannot be empty.")
        self.notes.append(note)

    def delete_note(self, index: int):
        if not (0 <= index < len(self.notes)):
            raise IndexError("Note index is out of range.")
        self.notes.pop(index)

    def find_notes_by_text(self, keyword: str):
        return [note for note in self.notes if keyword.lower() in note.text.lower()]

    def find_notes_by_tag(self, tag: str):
        if not tag.strip():
            raise ValueError("Tag cannot be empty.")
        return [note for note in self.notes if tag.lower() in note.tags]

    
    def sort_notes_by_tags(self):
        if not self.notes:
            return "No notes to sort."

        groups = {}
        no_tag_key = "x_no_tags"

        for note in self.notes:
            if note.tags and len(note.tags) > 0:
                all_tags_of_note = sorted(note.tags)
                first_tag = all_tags_of_note[0]
            else:
                first_tag = no_tag_key

            if first_tag not in groups:
                groups[first_tag] = []
            groups[first_tag].append(note)

        sorted_keys = list(groups.keys())
        sorted_keys.sort()
    
        final_string = ""
        for key in sorted_keys:
            if key == no_tag_key:
                display_name = "NO TAGS:"
            else:
                display_name = key.upper() + ":"
        
            final_string = final_string + display_name + "\n"

            notes_in_group = groups[key]
            notes_in_group.sort(key=lambda x: x.text.lower())

            for n in notes_in_group:
                final_string = final_string + "  - " + n.text + "\n"

        return final_string.strip()
    
    def edit_note_text(self, index: int, new_text: str):
        if not (0 <= index < len(self.notes)):
            raise IndexError("Note index is out of range.")
        if not new_text.strip():
            raise ValueError("New text cannot be empty.")
        self.notes[index].edit_text(new_text)