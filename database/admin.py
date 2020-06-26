from django.contrib import admin

# Importing all models
from .models import PaceUser, SchoolClass, Mission

# Register your models here.

admin.site.register(PaceUser)
admin.site.register(SchoolClass)
admin.site.register(Mission)
