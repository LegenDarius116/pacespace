from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# use to specify directory path, temporary for now
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class SchoolClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
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

    description_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    submission = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    date_assign = models.DateTimeField(auto_now_add=True)

    date_due = models.DateTimeField(default=timezone.now)

    date_submit = models.DateTimeField(null=True, blank=True)


class PaceUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_classes = models.ManyToManyField(SchoolClass)
