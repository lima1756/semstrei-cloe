from .DataNotValidException import DataNotValidException


class InputValidation:

    errors = {}
    fail = False

    def __init__(self, data_to_validate, validators):
        self.data = data_to_validate
        self.validators = validators

    def validate(self):
        for key in self.validators:
            self.errors[key] = []
            for validator in self.validators[key]:
                try:
                    self.data[key] = validator.validate(self.data[key])
                except DataNotValidException as e:
                    self.fail = True
                    self.errors[key].append(validator.get_error())
        if self.fail:
            raise DataNotValidException(
                "Some of the validations failed, please review the error")
        return self.data

    def get_error(self):
        if not self.fail:
            return None
        else:
            return self.errors
