from django.contrib import admin

# Importing all models
from .models import User, SchoolClass, Mission, Project # importing all user types

# Register your models here.

admin.site.register(User)
admin.site.register(SchoolClass)
admin.site.register(Mission)
admin.site.register(Project)
