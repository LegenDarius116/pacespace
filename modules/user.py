from django.db import models
from django.contrib.auth.models import User, AbstractUser
from modules.schoolclass import SchoolClass

# if we want to just have boolean field to separate users
# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     school_classes = models.ManyToManyField(SchoolClass, null=True)
#     reward = models.IntegerField(default=0)


# Abstract UserType model/class
# use function userTypeChecker
class UserType(models.Model):
    """Denotes a user type for our app, which can either be Student or Teacher"""

    # links this class to an actual account
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # connects this user to 0 or more classes
    school_classes = models.ManyToManyField(SchoolClass, null=True)

    def __str__(self):
        return str(self.user)

    # Makes sure it is an abstract user model/class
    class Meta:
        abstract = True


class Student(UserType):
    reward = models.IntegerField(default=0)


class Teacher(UserType):
    pass
