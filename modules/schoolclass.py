from django.db import models
from django.utils import timezone

class SchoolClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

# project is made up of mission components
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

    submission = models.FileField(upload_to="temp", null=True, blank=True)

    reward = models.IntegerField(default=0)

    


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

    submission = models.FileField(upload_to="", null=True, blank=True)

    missions = models.ManyToManyField(Mission, null=True)

    date_assign = models.DateTimeField(default=timezone.now)

    date_due = models.DateTimeField(default=timezone.now)
