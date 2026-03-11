# Parent class Field for Record fields like Name, Phone, Birthday

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)