from django.db import models
from django.contrib.auth.models import AbstractUser
from modules.schoolclass import *


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_classes = models.ManyToManyField(SchoolClass, null=True)
