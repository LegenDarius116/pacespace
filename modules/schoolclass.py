from django.db import models

class SchoolClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

    
class Project(models.Model):
    STATUS_CHOICES = [
        ('A', 'Assigned'),
        ('S', 'Submitted'),
        ('O', 'Overdue')
    ]    

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A"
    ) 

    submission = models.FileField(upload_to="", null=True, blank=True)

    missions = models.ManyToManyField(Mission, null=True)

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

    submission = models.FileField(upload_to="", null=True, blank=True)

    reward = models.IntegerField(default=0)