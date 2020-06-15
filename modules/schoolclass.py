from django.db import models
from django.utils import timezone


class SchoolClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


# use to specify directory path, temporary for now
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


# Project is made up of many Missions
class Mission(models.Model):
    STATUS_CHOICES = [
        ('A', 'Assigned'),
        ('C', 'Completed')
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A"
    )   

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    description_text = models.TextField(default='')

    submission = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    reward = models.IntegerField(default=0)
    
    date_assign = models.DateTimeField(auto_now_add=True)

    date_due = models.DateTimeField(default=timezone.now)

    date_submit = models.DateTimeField(null=True, blank=True)


class Project(models.Model):
    STATUS_CHOICES = [
        ('A', 'Assigned'),
        ('S', 'Submitted'),
        ('O', 'Overdue'),
        ('SL', 'Submitted Late')
    ]    

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A"
    ) 

    description_text = models.TextField(default='', null=True, blank=True)

    description_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    # maybe these fields can be taken by last mission?
    # but also it may be that these are separate, as missions are optional
    submission = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    date_assign = models.DateTimeField(auto_now_add=True)

    date_due = models.DateTimeField(default=timezone.now)

    date_submit = models.DateTimeField(null=True, blank=True)
