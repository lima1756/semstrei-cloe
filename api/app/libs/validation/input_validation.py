from .DataNotValidException import DataNotValidException


class InputValidation:

    errors = {}
    fail = False

    def __init__(self, data_to_validate, validators, must_have_key=False):
        self.data = data_to_validate
        self.validators = validators
        self.must_have_key = must_have_key

    def validate(self):
        for key in self.validators:
            self.errors[key] = []
            for validator in self.validators[key]:
                if not self.must_have_key and not key in self.data:
                    continue
                elif not key in self.data:
                    self.errors[key].append("value not provided")
                    continue
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
