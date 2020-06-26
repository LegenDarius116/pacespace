from database.models import SchoolClass, PaceUser, Project, ProjectSubmission
from datetime import datetime


def create_class(teacher: PaceUser, name: str):
    """If a user is logged in as a Teacher, this function creates a new class
    and adds it to the user's schoolclasses.
    """
    if teacher.is_teacher:
        schoolclass = SchoolClass(name=name, teacher=teacher)
        schoolclass.save()
        teacher.schoolclasses.add(schoolclass)


def add_student_to_class(teacher: PaceUser, schoolclass: SchoolClass, student: PaceUser):
    """Adds student (PaceUser) to a class only if a user is logged in as a Teacher."""
    if not teacher.is_teacher:
        print("Error: User is not logged in as a Teacher!")
        return

    if not student.is_student:
        print("Error: Cannot add another teacher to this class!")
        return

    if schoolclass not in teacher.schoolclasses.all():
        print("Error: Cannot add student to a class you are not the teacher of!")
        return

    # if none of the errors above go off, perform the actual operation
    student.schoolclasses.add(schoolclass)
    student.save()
    schoolclass.student_count += 1
    schoolclass.save()

def assign_project(teacher: PaceUser, schoolclass: SchoolClass, assignment_description: str, due_date: datetime):
    """Use this function to allow a teacher to assign projects for classes they own"""
    if teacher.is_teacher and teacher == schoolclass.teacher:
        project = Project(
            description_text=assignment_description,
            date_due=due_date,
            schoolclass=schoolclass
        )
        project.save()

    else:
        print("Error: Cannot add project to a class you are not the teacher of!")
        return


def submit_project(student: PaceUser, project: Project, content: str):
    """Allows Students to submit Projects for their SchoolClass"""
    if not student.is_student:
        print("Error: Non-students cannot submit projects.")
        return

    if project.schoolclass not in student.schoolclasses.all():
        print("Error: Cannot submit to a project that belongs to a class you are not enrolled in!")
        return

    submission = ProjectSubmission(
        student=student,
        project=project,
        content=content,
        date_submit=datetime.now(),
    )
    submission.save()


def grade_submission(teacher: PaceUser, submission: ProjectSubmission, grade: int):
    """Allows Teachers to grade project submissions"""
    if submission.project.schoolclass not in teacher.schoolclasses.all():
        print("Error: Submission does not belong to a class that the teacher is teaching.")
        return

    submission.grade = grade
    submission.save()
