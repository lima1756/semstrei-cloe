import unittest
from ..base_test_app import BaseTestApp
from app.models.Role import Role
from app.models.UserData import UserData
from app import App


class TestRoleModel(BaseTestApp):

    def test_setting_a_role(self):
        role = Role(1, "TI")
        user = UserData(
            email='test@test.com',
            password='test',
            name="test name",
            phone_number="1234567",
            role=1
        )
        with self.app.app_context():
            self.db.session.add(role)
            self.db.session.add(user)
            self.db.session.commit()
            self.assertTrue(user.role.name == "TI")
            # cleaning up
            self.db.session.delete(role)
            self.db.session.delete(user)
            self.db.session.commit()
