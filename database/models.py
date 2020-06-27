from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from datetime import date

class SchoolClass(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey('PaceUser', on_delete=models.SET_NULL, null=True)
    student_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('view_schoolclass', args=self.pk)


def user_directory_path(instance, filename):
    '''use to specify directory path for mission creation'''
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.schoolclass.teacher.id, filename)

def submission_directory_path(instance, filename):
    '''use to specify directory path for mission submission'''
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.student.id, filename)


class Mission(models.Model):
    name = models.TextField(default='Mission')
    description = models.TextField(default='', null=True, blank=True)
    instructions = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    date_assign = models.DateField(auto_now_add=True)
    date_due = models.DateField(default=date.today)
    schoolclass = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('view_mission', kwargs={'pk_class': self.schoolclass.pk, 'pk_mission':self.pk})



class PaceUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    schoolclasses = models.ManyToManyField(SchoolClass)


class MissionSubmission(models.Model):
    """A mission submission given by a Student"""
    student = models.ForeignKey(PaceUser, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    date_submit = models.DateField(auto_now_add=True)
    message = models.TextField(default='')
    file_submission = models.FileField(upload_to=submission_directory_path, null=True, blank=True)
    grade = models.IntegerField(default=-1)
