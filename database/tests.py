from django.test import TestCase
from database.models import SchoolClass, PaceUser, Mission, MissionSubmission
from database.user_functions import add_student_to_class, create_class, assign_mission, submit_mission, grade_submission
from datetime import datetime, timedelta


class UserTestCase(TestCase):
    def setUp(self):
        """Creates a test student and test teacher. I believe these are automatically deleted because Django
        will put these in a temporary test database.
        """
        self.student = PaceUser(
            username="test_student",
            email="student@test.com",
            password="password_password",
            is_student=True,
            is_teacher=False
        )

        self.teacher = PaceUser(
            username="test_teacher",
            email="teacher@test.com",
            password="password_password",
            is_student=False,
            is_teacher=True
        )

        self.teacher2 = PaceUser(
            username="test_teacher_2",
            email="teacher2@test.com",
            password="password_password",
            is_student=False,
            is_teacher=True
        )

        self.student.save()
        self.teacher.save()
        self.teacher2.save()

    def test_create_class_happy(self):
        """Tests that Teachers can create School Classes"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        self.assertTrue(self.teacher.schoolclasses.get(name="History of Jamaica"))
        print(self.teacher.schoolclasses.all())

    def test_add_student_to_class(self):
        """Tests happy path of a Teacher adding a Student to a class they teach."""

        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        for user in (self.teacher, self.student):
            self.assertTrue(user.schoolclasses.get(name="History of Jamaica"))

    def test_student_cannot_create_class(self):
        """Tests that Students cannot create classes"""
        create_class(teacher=self.student, name="History of Jamaica")

        self.assertFalse(self.student.schoolclasses.all())
        with self.assertRaises(Exception):
            SchoolClass.objects.get(name="History of Jamaica")

    def test_cannot_add_another_teacher(self):
        """Tests that Teachers cannot add another Teacher to their class."""
        create_class(teacher=self.teacher, name="Aggressive Hacking")
        schoolclass = SchoolClass.objects.get(name="Aggressive Hacking")
        add_student_to_class(teacher=self.teacher, student=self.teacher2, schoolclass=schoolclass)

        self.assertFalse(self.teacher2.schoolclasses.all())

    def test_cannot_add_to_class(self):
        """Tests that Teachers cannot add students to a class that they are not instructing."""
        SchoolClass.objects.create(name="Not My Class")
        schoolclass = SchoolClass.objects.get(name="Not My Class")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        self.assertFalse(self.teacher.schoolclasses.all())
        self.assertFalse(self.student.schoolclasses.all())

    def test_assign_mission_happy(self):
        """Tests that teachers can assign missions to classes they instruct"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_mission(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        mission = Mission.objects.get(description_text="Assignment Description")

        self.assertEqual(mission.schoolclass, schoolclass)

    def test_assign_mission_fail(self):
        """Tests that teachers cannot assign missions to classes they don't teach"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_mission(
            teacher=self.teacher2,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        with self.assertRaises(Exception):
            Mission.objects.get(description_text="Assignment Description")

        self.assertFalse(Mission.objects.filter(schoolclass=schoolclass))

    def test_mission_submission_happy(self):
        """Tests that students can upload Mission Submissions for a class they're in."""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_mission(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        mission = Mission.objects.get(description_text="Assignment Description")
        submit_mission(student=self.student, mission=mission, content="Mission Submission Content")
        submission = MissionSubmission.objects.get(
            student=self.student,
            mission=mission,
            content="Mission Submission Content"
        )

        self.assertEqual(submission.mission, mission)
        self.assertEqual(submission.student, self.student)
        self.assertEqual(submission.grade, -1)
        self.assertIn(submission.mission.schoolclass, self.student.schoolclasses.all())

    def test_mission_submission_to_invalid_class(self):
        """Tests that students cannot upload Mission Submissions to classes they're not in."""
        schoolclass = SchoolClass(name="asdf")
        mission = Mission(schoolclass=schoolclass)
        submit_mission(student=self.student, content="asd", mission=mission)

        with self.assertRaises(Exception):
            MissionSubmission.objects.get(
                student=self.student,
                mission=mission,
                content="asd",
            )

    def test_mission_submission_invalid_user(self):
        """Tests that teachers cannot upload Mission Submissions"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        assign_mission(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        mission = Mission.objects.get(description_text="Assignment Description")

        submit_mission(student=self.teacher, mission=mission, content="Mission Submission")

        with self.assertRaises(Exception):
            MissionSubmission.objects.get(
                student=self.teacher,
                mission=mission,
                content="Mission Submission",
            )

    def test_grade_submission_happy(self):
        """Tests that teachers can grade Mission Submissions"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_mission(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        mission = Mission.objects.get(description_text="Assignment Description")

        submit_mission(student=self.student, mission=mission, content="Mission Submission Content")
        submission = MissionSubmission.objects.get(
            student=self.student,
            mission=mission,
            content="Mission Submission Content"
        )

        grade_submission(teacher=self.teacher, submission=submission, grade=100)

    def test_grade_submission_invalid(self):
        """Tests that Teachers cannot grade Mission Submissions to classes they don't teach."""
        create_class(teacher=self.teacher, name="History of Cuba")
        schoolclass = SchoolClass.objects.get(name="History of Cuba")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_mission(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        mission = Mission.objects.get(description_text="Assignment Description")

        submit_mission(student=self.student, mission=mission, content="Mission Submission Content")
        submission = MissionSubmission.objects.get(
            student=self.student,
            mission=mission,
            content="Mission Submission Content"
        )

        grade_submission(teacher=self.teacher2, submission=submission, grade=100)
        self.assertEqual(submission.grade, -1)
