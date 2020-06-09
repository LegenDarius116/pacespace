from unittest import TestCase
from context import User, Student, Teacher


class TestUsers(TestCase):
    def test_cannot_instantiate_user_class(self):
        """Ensure that attempting to instantiate the User Class throws an error"""
        with self.assertRaises(TypeError):
            User(user_name='asdasd', user_id=12345)

