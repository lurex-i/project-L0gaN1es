class Address:
    def __init__(self, value:str):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if not val or not val.strip():
            raise Exception("Address can't be empty")
        self.__value = val.strip()

    def __str__(self):
        return str(self.value)

   