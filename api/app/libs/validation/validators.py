import re
import datetime
from . import DataNotValidException


class Validator:
    error = None

    @classmethod
    def validate(cls, input):
        raise NotImplementedError()

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class Strip(Validator):
    @classmethod
    def validate(cls, input):
        if input is None:
            return None
        try:
            cls.error = None
            return input.strip()
        except:
            cls.error = "String not trimmable"
            raise DataNotValidException()


class ValidateEmail(Validator):
    @classmethod
    def validate(cls, input):
        s = re.search(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,10}$", input)
        if s is None:
            cls.error = "Not valid email"
            raise DataNotValidException()
        cls.error = None
        return input


class ValidatePassword(Validator):
    @classmethod
    def validate(cls, input):
        s = re.search(
            r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!%^&,._+-]).{6,32}$", input)
        if s is None:
            cls.error = "Password must contain one lowercase letter, uppercase, number, a symbol (*.!%^&,._+-) and be at least 6 characters, maximum 32"
            raise DataNotValidException()
        cls.error = None
        return input


class ValidateNotEmpty(Validator):
    @classmethod
    def validate(cls, input):
        if input is None:
            cls.error = "Input must not be empty"
            raise DataNotValidException()
        s = re.search(r"^.+$", str(input))
        if s is None:
            cls.error = "Input must not be empty"
            raise DataNotValidException()
        cls.error = None
        return input


class ValidateAlphabeticString(Validator):
    @classmethod
    def validate(cls, input):
        if input is None:
            return None
        s = re.search(
            r"^[a-zA-Z ]*$", input)
        if s is None:
            cls.error = "Not valid alphabetic"
            raise DataNotValidException()
        cls.error = None
        return input


class ValidateNumber(Validator):
    @classmethod
    def validate(cls, input):
        try:
            float(input)
            cls.error = None
            return input
        except ValueError:
            cls.error = "Input is not a number"
            raise DataNotValidException()


class ValidateInteger(Validator):
    @classmethod
    def validate(cls, input):
        if str(input).isnumeric():
            cls.error = None
            return input
        cls.error = "Input is not an integer"
        raise DataNotValidException()


class ValidateDate(Validator):
    @classmethod
    def validate(cls, input):
        try:
            datetime.datetime.strptime(input, '%d-%b-%Y')
            cls.error = None
            return input
        except ValueError:
            cls.error = "Date not in correct format, dd-MMM-YYY (e.j. 12-Jan-2020)"
            raise DataNotValidException()
