from . import DataNotValidException

class InputValidation:

    errors = {}

    def __init__(self, data_to_validate, validators):
        self.data = data_to_validate
        self.validators = validators

    def validate(self):
        for key, value in self.validators:
            self.errors[key] = []
            for validator in value:
                try:
                    self.data[key] = validator.validate(self.data[key])
                except DataNotValidException:
                    self.errors[key].append(validator.get_error())
        if bool(self.errors):
            raise DataNotValidException(
                "Some of the validations failed, please review the error")
        return self.data

    def get_error(self):
        if not bool(self.errors):
            return None
        else:
            return self.errors
