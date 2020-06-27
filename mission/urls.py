from django.urls import path
from . import views


urlpatterns = [
    #for teacher
    path('class/<int:pk>/mission', views.class_mission, name='class_mission'),
    
    #for student
    path('mission/all', views.all_mission, name='all_mission'),
    
    #both
    path('mission/<int:pk>', views.view_mission, name='view_mission'),
]