from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class SchoolClass(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey('PaceUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'


# use to specify directory path, temporary for now
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class SchoolClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    # because of ProjectSubmission, might remove these
    STATUS_CHOICES = [
        ('A', 'Assigned'),
        ('S', 'Submitted'),
        ('O', 'Overdue'),
        ('SL', 'Submitted Late')
    ]    

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="A"
    )

    description_text = models.TextField(default='', null=True, blank=True)

    # might remove this for simplicity
    description_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    date_assign = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(default=timezone.now)

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)


class PaceUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_classes = models.ManyToManyField(SchoolClass)


class ProjectSubmission(models.Model):
    """A project submission given by a Student"""
    student = models.ForeignKey(PaceUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_submit = models.DateTimeField()
    content = models.TextField(default='')
    grade = models.IntegerField(default=-1)
