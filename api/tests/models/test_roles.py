import unittest
from ..base import BaseTestCase
BaseTestCase.create_app()
from app.models.Role import Role
from app.models.UserData import UserData
from app import App

db = App.get_instance().db


class TestRoleModel(BaseTestCase):
    
    def test_setting_a_role(self):
        role = Role(1, "TI")
        user = UserData(
            email='test@test.com',
            password='test',
            name="test name",
            phone_number="1234567",
            role=1
        )
        db.session.add(role)
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.role.name == "TI")
        # cleaning up
        db.session.delete(role)
        db.session.delete(user)
        db.session.commit()

