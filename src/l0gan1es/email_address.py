from email_validator import validate_email, EmailNotValidError

class EmailAddress:
    def __init__(self, value:str):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if not self.is_email_valid(val):
            raise Exception("Email not valid")
        self.__value = val 

    def __str__(self):
        return str(self.value)

    @staticmethod
    def is_email_valid(email: str) -> bool: 
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
        
    if __name__ == "__main__":
        print(is_email_valid("user-123@gmail.com"))
        print(is_email_valid("email@i"))