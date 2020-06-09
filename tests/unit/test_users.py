from unittest import TestCase
from context import User, Student, Teacher


class TestUsers(TestCase):
    def test_cannot_instantiate_user_class(self):
        """Ensure that attempting to instantiate the User Class throws an error"""
        with self.assertRaises(TypeError):
            User(name='asdasd', id=12345)

    def test_student_happy(self):
        student = Student(name='Jeff', id=420)
        self.assertEqual(student.id, 420)
        self.assertEqual(student.name, 'Jeff')
