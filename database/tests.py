from django.test import TestCase
from database.models import SchoolClass, PaceUser
from database.user_functions import add_student_to_class, create_class


class UserTestCase(TestCase):
    def setUp(self):
        """Creates a test student and test teacher. I believe these are automatically deleted because Django
        will put these in a temporary test database.
        """
        PaceUser.objects.create_user(
            username="test_student",
            email="student@test.com",
            password="password_password",
            is_student=True,
            is_teacher=False
        )

        PaceUser.objects.create_user(
            username="test_teacher",
            email="teacher@test.com",
            password="password_password",
            is_student=False,
            is_teacher=True
        )

        PaceUser.objects.create_user(
            username="test_teacher_2",
            email="teacher@test.com",
            password="password_password",
            is_student=False,
            is_teacher=True
        )

    def test_create_class_happy(self):
        """Tests that Teachers can create School Classes"""
        teacher = PaceUser.objects.get(username="test_teacher")
        create_class(teacher=teacher, name="History of Jamaica")
        self.assertTrue(teacher.school_classes.get(name="History of Jamaica"))
        print(teacher.school_classes.all())

    def test_add_student_to_class(self):
        """Tests happy path of a Teacher adding a Student to a class they teach."""
        teacher = PaceUser.objects.get(username="test_teacher")
        student = PaceUser.objects.get(username="test_student")

        create_class(teacher=teacher, name="History of Jamaica")
        school_class = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=teacher, student=student, school_class=school_class)

        for user in (teacher, student):
            self.assertTrue(user.school_classes.get(name="History of Jamaica"))

    def test_student_cannot_create_class(self):
        """Tests that Students cannot create classes"""
        student = PaceUser.objects.get(username="test_student")
        create_class(teacher=student, name="History of Jamaica")
        self.assertFalse(student.school_classes.all())

    def test_cannot_add_another_teacher(self):
        """Tests that Teachers cannot add another Teacher to their class."""
        teacher = PaceUser.objects.get(username="test_teacher")
        teacher_2 = PaceUser.objects.get(username="test_teacher_2")

        create_class(teacher=teacher, name="Aggressive Hacking")
        school_class = SchoolClass.objects.get(name="Aggressive Hacking")
        add_student_to_class(teacher=teacher, student=teacher_2, school_class=school_class)

        self.assertFalse(teacher_2.school_classes.all())

    def test_cannot_add_to_class(self):
        """Tests that Teachers cannot add students to a class that they are not instructing."""
        teacher = PaceUser.objects.get(username="test_teacher")
        student = PaceUser.objects.get(username="test_student")

        SchoolClass.objects.create(name="Not My Class")
        school_class = SchoolClass.objects.get(name="Not My Class")
        add_student_to_class(teacher=teacher, student=student, school_class=school_class)

        self.assertFalse(teacher.school_classes.all())
        self.assertFalse(student.school_classes.all())
