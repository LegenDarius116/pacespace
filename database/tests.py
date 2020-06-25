from django.test import TestCase
from database.models import SchoolClass, PaceUser, Project, ProjectSubmission
from database.user_functions import add_student_to_class, create_class, assign_project, submit_project, grade_submission
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

    def test_assign_project_happy(self):
        """Tests that teachers can assign projects to classes they instruct"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_project(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        project = Project.objects.get(description_text="Assignment Description")

        self.assertEqual(project.schoolclass, schoolclass)

    def test_assign_project_fail(self):
        """Tests that teachers cannot assign projects to classes they don't teach"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_project(
            teacher=self.teacher2,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        with self.assertRaises(Exception):
            Project.objects.get(description_text="Assignment Description")

        self.assertFalse(Project.objects.filter(schoolclass=schoolclass))

    def test_project_submission_happy(self):
        """Tests that students can upload Project Submissions for a class they're in."""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_project(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )

        project = Project.objects.get(description_text="Assignment Description")
        submit_project(student=self.student, project=project, content="Project Submission Content")
        submission = ProjectSubmission.objects.get(
            student=self.student,
            project=project,
            content="Project Submission Content"
        )

        self.assertEqual(submission.project, project)
        self.assertEqual(submission.student, self.student)
        self.assertEqual(submission.grade, -1)
        self.assertIn(submission.project.schoolclass, self.student.schoolclasses.all())

    def test_project_submission_to_invalid_class(self):
        """Tests that students cannot upload Project Submissions to classes they're not in."""
        schoolclass = SchoolClass(name="asdf")
        project = Project(schoolclass=schoolclass)
        submit_project(student=self.student, content="asd", project=project)

        with self.assertRaises(Exception):
            ProjectSubmission.objects.get(
                student=self.student,
                project=project,
                content="asd",
            )

    def test_project_submission_invalid_user(self):
        """Tests that teachers cannot upload Project Submissions"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        assign_project(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        project = Project.objects.get(description_text="Assignment Description")

        submit_project(student=self.teacher, project=project, content="Project Submission")

        with self.assertRaises(Exception):
            ProjectSubmission.objects.get(
                student=self.teacher,
                project=project,
                content="Project Submission",
            )

    def test_grade_submission_happy(self):
        """Tests that teachers can grade Project Submissions"""
        create_class(teacher=self.teacher, name="History of Jamaica")
        schoolclass = SchoolClass.objects.get(name="History of Jamaica")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_project(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        project = Project.objects.get(description_text="Assignment Description")

        submit_project(student=self.student, project=project, content="Project Submission Content")
        submission = ProjectSubmission.objects.get(
            student=self.student,
            project=project,
            content="Project Submission Content"
        )

        grade_submission(teacher=self.teacher, submission=submission, grade=100)

    def test_grade_submission_invalid(self):
        """Tests that Teachers cannot grade Project Submissions to classes they don't teach."""
        create_class(teacher=self.teacher, name="History of Cuba")
        schoolclass = SchoolClass.objects.get(name="History of Cuba")
        add_student_to_class(teacher=self.teacher, student=self.student, schoolclass=schoolclass)

        assign_project(
            teacher=self.teacher,
            schoolclass=schoolclass,
            assignment_description="Assignment Description",
            due_date=datetime.now() + timedelta(days=50)
        )
        project = Project.objects.get(description_text="Assignment Description")

        submit_project(student=self.student, project=project, content="Project Submission Content")
        submission = ProjectSubmission.objects.get(
            student=self.student,
            project=project,
            content="Project Submission Content"
        )

        grade_submission(teacher=self.teacher2, submission=submission, grade=100)
        self.assertEqual(submission.grade, -1)
