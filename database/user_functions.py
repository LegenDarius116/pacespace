from database.models import SchoolClass, PaceUser


def create_class(teacher: PaceUser, name: str):
    """If a user is logged in as a Teacher, this function creates a new class
    and adds it to the user's school_classes.
    """
    if teacher.is_teacher:
        school_class = SchoolClass(name=name)
        school_class.save()
        teacher.school_classes.add(school_class)


def add_student_to_class(teacher: PaceUser, school_class: SchoolClass, student: PaceUser):
    """Adds student (PaceUser) to a class only if a user is logged in as a Teacher."""
    if not teacher.is_teacher:
        print("Error: User is not logged in as a Teacher!")
        return

    if not student.is_student:
        print("Error: Cannot add another teacher to this class!")
        return

    if school_class not in teacher.school_classes.all():
        print("Error: Cannot add student to a class you are not the teacher of!")
        return

    # if none of the errors above go off, perform the actual operation
    student.school_classes.add(school_class)
    student.save()
