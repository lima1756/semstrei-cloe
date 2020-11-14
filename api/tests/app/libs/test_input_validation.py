import unittest
import logging

import app.libs.validation as validation
from ..base_test_app import BaseTestApp


class TestInputValidation(BaseTestApp):

    def test_strip(self):
        s = validation.Strip.validate("   asdf     ")
        self.assertEqual(len(s), 4, "Strip didn't work")

    def test_password(self):
        s = validation.ValidatePassword.validate("aA1-asdf")
        self.assertEqual(s, "aA1-asdf")
        self.assertIsNone(validation.ValidatePassword.get_error())

    def test_password_fail_not_long(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidatePassword.validate, "aA1-")

    def test_password_fail_not_requirements(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidatePassword.validate, "asdfzxcv")

    def test_password_fail_not_short(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidatePassword.validate, "aA1-qwerqwerqwerqwerqwerqwerqwerqwerqwer")

    def test_email(self):
        s = validation.ValidateEmail.validate("luis@mail.com")
        self.assertEqual(s, "luis@mail.com")
        self.assertIsNone(validation.ValidateEmail.get_error())

    def test_email_fail_not_valid(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidateEmail.validate, "asdfzxcv")

    def test_not_empty(self):
        s = validation.ValidateNotEmpty.validate("asdf")
        self.assertEqual(s, "asdf")
        self.assertIsNone(validation.ValidateNotEmpty.get_error())

    def test_not_empty_fail(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidateNotEmpty.validate, "")

    def test_alphabetical(self):
        s = validation.ValidateAlphabeticString.validate("as df")
        self.assertEqual(s, "as df")
        self.assertIsNone(validation.ValidateAlphabeticString.get_error())

    def test_alphabetical_fail(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidateAlphabeticString.validate, "1234")

    def test_number(self):
        s = validation.ValidateNumber.validate("3.141592")
        self.assertEqual(s, "3.141592")
        self.assertIsNone(validation.ValidateNumber.get_error())

    def test_number_fail(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidateNumber.validate, "asdf")

    def test_integer(self):
        s = validation.ValidateInteger.validate("5")
        self.assertEqual(s, "5")
        self.assertIsNone(validation.ValidateInteger.get_error())

    def test_integer_fail(self):
        self.assertRaises(validation.DataNotValidException,
                          validation.ValidateInteger.validate, "asdf")

    def test_input_validation(self):
        validator = validation.InputValidation({"name": "asdf", "mail": "lm@mail.com"}, {"name": [
                                               validation.Strip, validation.ValidateAlphabeticString], "mail": [validation.Strip, validation.ValidateEmail]})
        data = validator.validate()
        self.assertEqual(data['name'], 'asdf')
        self.assertEqual(data['mail'], 'lm@mail.com')

    def test_input_validation_fail(self):
        validator = validation.InputValidation({"name": "1234", "mail": "asdf"}, {"name": [
                                               validation.Strip, validation.ValidateAlphabeticString], "mail": [validation.Strip, validation.ValidateEmail]})
        self.assertRaises(validation.DataNotValidException, validator.validate)
