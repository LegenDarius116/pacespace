from database.models import SchoolClass, PaceUser, Mission, MissionSubmission
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

def assign_mission(teacher: PaceUser, schoolclass: SchoolClass, description: str, due_date: datetime):
    """Use this function to allow a teacher to assign missions for classes they own"""
    if teacher.is_teacher and teacher == schoolclass.teacher:
        mission = Mission(
            description=description,
            date_due=due_date,
            schoolclass=schoolclass,
        )
        mission.save()

    else:
        print("Error: Cannot add mission to a class you are not the teacher of!")
        return


def submit_mission(student: PaceUser, mission: Mission, content: str):
    """Allows Students to submit Missions for their SchoolClass"""
    if not student.is_student:
        print("Error: Non-students cannot submit missions.")
        return

    if mission.schoolclass not in student.schoolclasses.all():
        print("Error: Cannot submit to a mission that belongs to a class you are not enrolled in!")
        return

    submission = MissionSubmission(
        student=student,
        mission=mission,
        content=content,
        date_submit=datetime.now(),
    )
    submission.save()


def grade_submission(teacher: PaceUser, submission: MissionSubmission, grade: int):
    """Allows Teachers to grade mission submissions"""
    if submission.mission.schoolclass not in teacher.schoolclasses.all():
        print("Error: Submission does not belong to a class that the teacher is teaching.")
        return

    submission.grade = grade
    submission.save()

def get_student_missions(student: PaceUser):
    all_schoolclass = student.schoolclasses.all()
    all_mission = {}

    for schoolclass in all_schoolclass:
        mission = Mission.objects.filter(schoolclass=schoolclass).exclude(missionsubmission__student=user)
        all_mission[schoolclass.name] = mission
    
    return all_mission
