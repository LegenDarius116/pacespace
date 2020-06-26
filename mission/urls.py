from django.urls import path
from . import views


urlpatterns = [
    path('class/<int:pk_class>/mission/<int:pk_mission>', views.view_mission, name='view_mission'),
    path('class/<int:pk>/mission/all', views.all_mission, name='all_mission'),
]