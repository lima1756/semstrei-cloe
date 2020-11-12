import re
from . import DataNotValidException


class Validator:
    error = None

    @classmethod
    def validate(cls, input):
        raise NotImplementedError()

    @classmethod
    def get_error(cls):
        raise NotImplementedError()


class Trim(Validator):

    @classmethod
    def validate(cls, input):
        try:
            return input.trim()
        except:
            cls.error = "String not trimmable"
            raise NotImplementedError()

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidateEmail(Validator):

    @classmethod
    def validate(cls, input):
        s = re.search(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,10}$", input)
        if s is None:
            cls.error = "Not valid email"
            raise DataNotValidException()
        return input

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidatePassword(Validator):
    @classmethod
    def validate(cls, input):
        s = re.search(
            r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!%^&,._+-]).{6,32}$", input)
        if s is None:
            cls.error = "Password must contain one lowercase letter, uppercase, number, a symbol (*.!%^&,._+-) and be at least 6 characters, maximum 32"
            raise DataNotValidException()
        return input

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidateNotEmpty(Validator):
    @classmethod
    def validate(cls, input):
        s = re.search(r"^.+$", input)
        if s is None:
            cls.error = "Input must not be empty"
            raise DataNotValidException()
        return input

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidateAlphabeticString(Validator):
    @classmethod
    def validate(cls, input):
        s = re.search(
            r"^[a-zA-Z ]+$", input)
        if s is None:
            cls.error = "Input must not be empty"
            raise DataNotValidException()
        return input

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidateNumber(Validator):
    @classmethod
    def validate(cls, input):
        if input.isNumeric():
            return input
        cls.error = "Input is not a number"
        raise DataNotValidException()

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err


class ValidateInteger(Validator):
    @classmethod
    def validate(cls, input):
        try:
            int(input)
            return input
        except ValueError:
            cls.error = "Input is not an integer"
            raise DataNotValidException()

    @classmethod
    def get_error(cls):
        err = cls.error
        cls.error = None
        return err
